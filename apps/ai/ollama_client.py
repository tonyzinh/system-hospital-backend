import os
import requests

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "30"))
OLLAMA_SYSTEM = os.getenv("OLLAMA_SYSTEM", "")


class OllamaError(Exception):
    pass


def chat_completion(
    messages, model: str | None = None, temperature: float = 0.2, max_tokens: int = 512
) -> str:
    """
    Chama /api/chat do Ollama.
    messages = [ {"role":"system"|"user"|"assistant", "content":"..."} ]
    """
    url = f"{OLLAMA_BASE_URL}/api/chat"

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
        resp = requests.post(url, json=payload, timeout=OLLAMA_TIMEOUT)
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
