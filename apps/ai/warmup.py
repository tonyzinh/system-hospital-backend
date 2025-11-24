"""
Sistema de pré-aquecimento do Ollama para reduzir latência da primeira pergunta.
"""

import logging
from .ollama_client import chat_completion, OllamaError

logger = logging.getLogger(__name__)


def warmup_ollama():
    """
    Faz uma pergunta simples para 'pré-aquecer' o modelo Ollama.
    Isso ajuda a reduzir a latência das primeiras perguntas reais.
    """
    try:
        # Pergunta muito simples para pré-aquecimento
        warmup_messages = [{"role": "user", "content": "Oi"}]

        # Usa configurações rápidas para warmup
        chat_completion(
            warmup_messages,
            temperature=0.1,
            max_tokens=50,
            timeout=30,  # Timeout curto para warmup
        )

        logger.info("Ollama pré-aquecido com sucesso")
        return True

    except OllamaError as e:
        logger.warning(f"Falha no pré-aquecimento do Ollama: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado no pré-aquecimento: {e}")
        return False


def is_ollama_ready():
    """
    Verifica se o Ollama está pronto para receber perguntas.
    """
    try:
        # Teste muito rápido
        test_messages = [{"role": "user", "content": "test"}]
        result = chat_completion(
            test_messages, temperature=0.1, max_tokens=10, timeout=15
        )
        return bool(result)

    except Exception:
        return False
