# Configurações de timeout
FAST_RESPONSE_TIMEOUT = 30  # Para perguntas simples
NORMAL_RESPONSE_TIMEOUT = 60  # Para perguntas normais
COMPLEX_RESPONSE_TIMEOUT = 120  # Para perguntas complexas

# Configurações de tokens
MIN_TOKENS = 256  # Para respostas muito curtas
FAST_TOKENS = 512  # Para perguntas simples
NORMAL_TOKENS = 1024  # Para perguntas normais
MAX_TOKENS = 2048  # Para perguntas complexas

# Limites para determinar complexidade
SHORT_QUESTION_LIMIT = 50  # caracteres
NORMAL_QUESTION_LIMIT = 200  # caracteres

# Cache settings
CACHE_SIZE_LIMIT = 100
CACHE_ENABLED = True

# Palavras-chave que indicam perguntas complexas
COMPLEX_KEYWORDS = [
    "explique detalhadamente",
    "análise completa",
    "comparação",
    "diferenças entre",
    "como funciona",
    "processo completo",
    "passo a passo",
    "tutorial",
    "exemplos",
]


def get_optimal_settings(question: str, history_length: int = 0):
    """
    Retorna configurações otimizadas baseadas na pergunta e histórico.

    Args:
        question: A pergunta do usuário
        history_length: Número de mensagens no histórico

    Returns:
        dict: Configurações otimizadas (tokens, timeout, temperature)
    """
    question_lower = question.lower()
    question_length = len(question)

    # Determina se é uma pergunta complexa
    is_complex = (
        question_length > NORMAL_QUESTION_LIMIT
        or any(keyword in question_lower for keyword in COMPLEX_KEYWORDS)
        or history_length > 5  # Conversas longas tendem a ser mais complexas
    )

    # Determina se é uma pergunta curta/simples
    is_short = question_length < SHORT_QUESTION_LIMIT

    if is_complex:
        return {
            "max_tokens": MAX_TOKENS,
            "timeout": COMPLEX_RESPONSE_TIMEOUT,
            "temperature": 0.3,  # Mais criatividade para respostas complexas
        }
    elif is_short:
        return {
            "max_tokens": FAST_TOKENS,
            "timeout": FAST_RESPONSE_TIMEOUT,
            "temperature": 0.1,  # Mais determinística para respostas rápidas
        }
    else:
        return {
            "max_tokens": NORMAL_TOKENS,
            "timeout": NORMAL_RESPONSE_TIMEOUT,
            "temperature": 0.2,  # Padrão
        }
