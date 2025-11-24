# Configurações de timeout (otimizadas para velocidade)
FAST_RESPONSE_TIMEOUT = 45  # Para perguntas simples (45 segundos)
NORMAL_RESPONSE_TIMEOUT = 60  # Para perguntas normais (60 segundos)
COMPLEX_RESPONSE_TIMEOUT = 90  # Para perguntas complexas (90 segundos)


# Configurações de tokens (reduzidas para maior velocidade)
MIN_TOKENS = 128  # Para respostas muito curtas
FAST_TOKENS = 256  # Para perguntas simples
NORMAL_TOKENS = 512  # Para perguntas normais
MAX_TOKENS = 1024  # Para perguntas complexas

# Limites para determinar complexidade
SHORT_QUESTION_LIMIT = 50  # caracteres
NORMAL_QUESTION_LIMIT = 200  # caracteres

# Cache settings
CACHE_SIZE_LIMIT = 100
CACHE_ENABLED = True

# Configurações de resiliência
MAX_RETRIES = 1  # Número máximo de tentativas
RETRY_DELAY = 0.5  # Delay entre tentativas em segundos
ENABLE_REQUEST_OPTIMIZATION = True  # Habilita otimizações de requisição

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
    Retorna configurações otimizadas para VELOCIDADE baseadas na pergunta.

    Args:
        question: A pergunta do usuário
        history_length: Número de mensagens no histórico

    Returns:
        dict: Configurações otimizadas priorizando velocidade
    """
    question_lower = question.lower()
    question_length = len(question)

    # Identifica perguntas médicas
    medical_keywords = [
        "medicamento",
        "remédio",
        "dipirona",
        "paracetamol",
        "ibuprofeno",
        "tratamento",
        "diagnóstico",
        "sintoma",
        "doença",
        "médico",
    ]

    # Identifica perguntas que precisam de respostas mais longas
    detailed_keywords = [
        "explique detalhadamente",
        "como funciona",
        "passo a passo",
        "tutorial",
        "processo completo",
        "análise completa",
    ]

    is_medical = any(keyword in question_lower for keyword in medical_keywords)
    needs_detail = any(keyword in question_lower for keyword in detailed_keywords)
    is_very_short = question_length < 20  # Perguntas muito curtas

    # Prioriza SEMPRE velocidade - máximo 1 minuto
    if is_very_short:
        return {
            "max_tokens": MIN_TOKENS,
            "timeout": FAST_RESPONSE_TIMEOUT,
            "temperature": 0.1,
            "fast_mode": True,
        }
    elif needs_detail:
        return {
            "max_tokens": MAX_TOKENS,
            "timeout": COMPLEX_RESPONSE_TIMEOUT,
            "temperature": 0.2,
            "fast_mode": False,
        }
    elif is_medical:
        return {
            "max_tokens": NORMAL_TOKENS,
            "timeout": NORMAL_RESPONSE_TIMEOUT,
            "temperature": 0.1,  # Mais precisão médica
            "fast_mode": False,
        }
    else:
        return {
            "max_tokens": FAST_TOKENS,
            "timeout": FAST_RESPONSE_TIMEOUT,
            "temperature": 0.1,
            "fast_mode": True,
        }
