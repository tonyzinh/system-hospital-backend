import os
import requests
import hashlib
import json
from .config import CACHE_SIZE_LIMIT, CACHE_ENABLED
# from functools import lru_cache

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))  # Aumentado para 2 minutos
OLLAMA_SYSTEM = os.getenv("OLLAMA_SYSTEM", "")

# Cache simples em memória para respostas
_response_cache = {}


class OllamaError(Exception):
    pass


def _get_cache_key(messages, model, temperature, max_tokens):
    """Gera uma chave de cache baseada nos parâmetros da requisição."""
    cache_data = {
        "messages": messages,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    cache_str = json.dumps(cache_data, sort_keys=True)
    return hashlib.md5(cache_str.encode()).hexdigest()


def _ollama_request(messages, model, temperature, max_tokens, timeout=None):
    """Faz a requisição real para o Ollama."""
    url = f"{OLLAMA_BASE_URL}/api/chat"
    request_timeout = timeout or OLLAMA_TIMEOUT

    # injeta system prompt no início, se definido e ainda não presente
    final_messages = list(messages or [])
    if OLLAMA_SYSTEM and (
        not final_messages or final_messages[0].get("role") != "system"
    ):
        final_messages = [{"role": "system", "content": OLLAMA_SYSTEM}] + final_messages

    payload = {
        "model": model or OLLAMA_MODEL,
        "messages": final_messages,
        "options": {"temperature": temperature, "num_predict": max_tokens},
        "stream": False,  # manter simples (resposta inteira)
    }

    try:
        resp = requests.post(url, json=payload, timeout=request_timeout)
    except requests.RequestException as e:
        raise OllamaError(
            f"Falha ao conectar no Ollama em {OLLAMA_BASE_URL}: {e}"
        ) from e

    if resp.status_code >= 400:
        raise OllamaError(f"Ollama retornou {resp.status_code}: {resp.text}")

    data = resp.json()
    # Resposta típica: {"message":{"role":"assistant","content":"..."},"done":true,...}
    content = (data.get("message") or {}).get("content", "")
    return content or ""


def chat_completion(
    messages,
    model: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
    timeout: int | None = None,
) -> str:
    """
    Chama /api/chat do Ollama com cache.
    messages = [ {"role":"system"|"user"|"assistant", "content":"..."} ]
    """
    # Usa timeout personalizado se fornecido, senão usa o padrão
    request_timeout = timeout or OLLAMA_TIMEOUT

    # Verifica se o cache está habilitado
    if not CACHE_ENABLED:
        return _ollama_request(
            messages, model, temperature, max_tokens, request_timeout
        )

    # Gera chave do cache
    cache_key = _get_cache_key(messages, model or OLLAMA_MODEL, temperature, max_tokens)

    # Verifica se já temos a resposta em cache
    if cache_key in _response_cache:
        return _response_cache[cache_key]

    # Faz a requisição se não estiver em cache
    result = _ollama_request(messages, model, temperature, max_tokens, request_timeout)

    # Armazena no cache (limita o tamanho do cache)
    if len(_response_cache) >= CACHE_SIZE_LIMIT:
        # Remove a entrada mais antiga
        oldest_key = next(iter(_response_cache))
        del _response_cache[oldest_key]

    _response_cache[cache_key] = result
    return result


def clear_cache():
    """Limpa o cache de respostas."""
    global _response_cache
    _response_cache.clear()


def get_cache_stats():
    """Retorna estatísticas do cache."""
    return {
        "size": len(_response_cache),
        "max_size": CACHE_SIZE_LIMIT,
        "enabled": CACHE_ENABLED,
    }
