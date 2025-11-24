import os
import requests
import hashlib
import json
from .config import CACHE_SIZE_LIMIT, CACHE_ENABLED
# from functools import lru_cache

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "300"))  # 5 minutos
OLLAMA_CONNECTION_TIMEOUT = int(
    os.getenv("OLLAMA_CONNECTION_TIMEOUT", "30")
)  # 30 segundos para conexão
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

    # Otimizações baseadas no tamanho da pergunta
    question_text = " ".join(
        [msg.get("content", "") for msg in final_messages if msg.get("role") == "user"]
    )

    # Para perguntas médicas, usar configurações específicas
    if any(
        word in question_text.lower()
        for word in ["medicamento", "remédio", "dipirona", "tratamento", "doença"]
    ):
        # Usar prompt médico se disponível
        medical_prompt = os.getenv("OLLAMA_MEDICAL_SYSTEM_PROMPT")
        if medical_prompt and (
            not final_messages or final_messages[0].get("role") != "system"
        ):
            final_messages = [
                {"role": "system", "content": medical_prompt}
            ] + final_messages

    payload = {
        "model": model or OLLAMA_MODEL,
        "messages": final_messages,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            # Otimizações para velocidade
            "num_ctx": 2048,  # Context window menor
            "num_batch": 512,  # Processamento em lote
            "num_thread": -1,   # Usar todos os threads disponíveis
            "use_mmap": True,   # Memory mapping para velocidade
            "use_mlock": True,  # Lock memory para performance
        },
        "stream": False,
    }

    try:
        # Usar timeout duplo: (conexão, leitura)
        timeout_tuple = (OLLAMA_CONNECTION_TIMEOUT, request_timeout)
        resp = requests.post(url, json=payload, timeout=timeout_tuple)

    except requests.exceptions.ConnectTimeout as e:
        raise OllamaError(
            f"Timeout de conexão com Ollama ({OLLAMA_CONNECTION_TIMEOUT}s): {e}"
        ) from e
    except requests.exceptions.ReadTimeout as e:
        raise OllamaError(
            f"Timeout de leitura com Ollama ({request_timeout}s): {e}"
        ) from e
    except requests.exceptions.Timeout as e:
        raise OllamaError(
            f"Timeout ao conectar com Ollama em {OLLAMA_BASE_URL}: {e}"
        ) from e
    except requests.RequestException as e:
        raise OllamaError(
            f"Erro ao conectar com Ollama em {OLLAMA_BASE_URL}: {e}"
        ) from e

    if resp.status_code >= 400:
        try:
            error_data = resp.json()
            error_msg = error_data.get("error", resp.text)
        except (ValueError, json.JSONDecodeError):
            error_msg = resp.text
        raise OllamaError(f"Ollama retornou {resp.status_code}: {error_msg}")

    try:
        data = resp.json()
    except ValueError as e:
        raise OllamaError(f"Resposta inválida do Ollama: {e}")

    # Resposta típica: {"message":{"role":"assistant","content":"..."},"done":true,...}
    message = data.get("message", {})
    content = message.get("content", "")

    if not content:
        # Tenta outros campos possíveis
        content = data.get("response", "") or data.get("text", "")

    return content or "Desculpe, não consegui gerar uma resposta."


def chat_completion(
    messages,
    model: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
    timeout: int | None = None,
) -> str:
    """
    Chama /api/chat do Ollama com cache e sistema de retry.
    messages = [ {"role":"system"|"user"|"assistant", "content":"..."} ]
    """
    # Usa timeout personalizado se fornecido, senão usa o padrão
    request_timeout = timeout or OLLAMA_TIMEOUT

    # Verifica se o cache está habilitado
    if CACHE_ENABLED:
        # Gera chave do cache
        cache_key = _get_cache_key(
            messages, model or OLLAMA_MODEL, temperature, max_tokens
        )

        # Verifica se já temos a resposta em cache
        if cache_key in _response_cache:
            return _response_cache[cache_key]

    # Sistema otimizado - uma tentativa rápida, sem retry para melhor UX
    try:
        result = _ollama_request(
            messages, model, temperature, max_tokens, request_timeout
        )

        # Armazena no cache se habilitado
        if CACHE_ENABLED:
            if len(_response_cache) >= CACHE_SIZE_LIMIT:
                # Remove a entrada mais antiga
                oldest_key = next(iter(_response_cache))
                del _response_cache[oldest_key]
            _response_cache[cache_key] = result

        return result

    except OllamaError as e:
        error_msg = str(e).lower()
        
        # Para timeouts, sugere reformular pergunta
        if "timeout" in error_msg or "timed out" in error_msg:
            raise OllamaError(
                f"Resposta demorou mais que {request_timeout}s. Tente uma pergunta mais simples."
            )
        else:
            raise e

    # Fallback - não deveria chegar aqui
    raise OllamaError("Falha inesperada na comunicação com Ollama")


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
