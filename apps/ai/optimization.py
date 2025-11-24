# Configurações adicionais para otimização do Ollama
OLLAMA_OPTIMIZATION_ENABLED = True

# Headers otimizados para melhor performance
OLLAMA_HEADERS = {
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Keep-Alive": "timeout=120, max=100",
}

# Pool de conexões para reutilização
REQUEST_POOL_SIZE = 10
REQUEST_POOL_MAX_SIZE = 20

# Configurações de modelo por contexto
MODEL_CONFIGS = {
    "medical": {
        "model": "llama3.1",
        "temperature": 0.1,  # Mais preciso para medicina
        "max_tokens": 1024,
        "system_prompt": "Você é um assistente médico especializado. Seja preciso e sempre recomende consultar um profissional.",
    },
    "general": {
        "model": "llama3.1",
        "temperature": 0.2,
        "max_tokens": 512,
        "system_prompt": "Você é um assistente útil e preciso.",
    },
    "simple": {
        "model": "llama3.1",
        "temperature": 0.1,
        "max_tokens": 256,
        "system_prompt": "Responda de forma concisa e direta.",
    },
}
