from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ollama_client import chat_completion, OllamaError, clear_cache, get_cache_stats
from .config import get_optimal_settings
from pathlib import Path
import hashlib


class AiChatView(APIView):
    """Chat endpoint que aceita histórico de mensagens e retorna completions."""

    def post(self, request):
        data = request.data or {}
        q = (data.get("question") or "").strip()
        history = data.get("history") or []
        model = data.get("model")

        if not q:
            return Response(
                {"detail": "question é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Monta mensagens válidas a partir do histórico
        messages = []
        if isinstance(history, list):
            for m in history:
                if (
                    isinstance(m, dict)
                    and m.get("role") in {"user", "assistant", "system"}
                    and m.get("content")
                ):
                    messages.append({"role": m["role"], "content": m["content"]})

        # Pergunta atual no final
        messages.append({"role": "user", "content": q})

        # Otimização baseada na complexidade da pergunta e histórico
        settings = get_optimal_settings(q, len(history))

        try:
            answer = chat_completion(
                messages,
                model=model,
                temperature=settings["temperature"],
                max_tokens=settings["max_tokens"],
                timeout=settings["timeout"],
            )
            return Response({"answer": answer})
        except OllamaError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class AiAnswerView(APIView):
    """Endpoint simples de resposta (compatibilidade)."""

    def post(self, request):
        data = request.data or {}
        q = (data.get("question") or "").strip()
        if not q:
            return Response(
                {"detail": "question é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Otimização baseada na complexidade da pergunta
            settings = get_optimal_settings(q)
            answer = chat_completion(
                [{"role": "user", "content": q}],
                temperature=settings["temperature"],
                max_tokens=settings["max_tokens"],
                timeout=settings["timeout"],
            )
            return Response({"answer": answer})
        except OllamaError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class AiAdvancedAnswerView(APIView):
    """Endpoint avançado (placeholder) — no momento usa apenas o Ollama para gerar respostas."""

    def post(self, request):
        data = request.data or {}
        question = (data.get("question") or "").strip()
        model = data.get("model")

        if not question:
            return Response(
                {"error": "Pergunta não pode estar vazia"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Atualmente apenas encaminha para o Ollama; integração RAG será adicionada depois.
        try:
            # Otimização baseada na complexidade da pergunta
            settings = get_optimal_settings(question)
            answer = chat_completion(
                [{"role": "user", "content": question}],
                model=model,
                temperature=settings["temperature"],
                max_tokens=settings["max_tokens"],
                timeout=settings["timeout"],
            )
            return Response({"answer": answer}, status=status.HTTP_200_OK)
        except OllamaError as e:
            return Response(
                {"error": "Erro interno no processamento", "details": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )


class AiIngestUrlView(APIView):
    """Endpoint de ingestão de URLs — implementação mínima para não quebrar importações.

    Se `url` for fornecida, cria um arquivo placeholder em `ai_data/web_txt/` com o conteúdo da URL.
    """

    def post(self, request):
        data = request.data or {}
        url = (data.get("url") or "").strip()
        if not url:
            return Response(
                {"error": "url é obrigatório"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Cria diretório e salva conteúdo placeholder
        base = Path("ai_data/web_txt")
        base.mkdir(parents=True, exist_ok=True)
        name = hashlib.md5(url.encode()).hexdigest() + ".txt"
        p = base / name
        p.write_text(f"Ingested placeholder for URL: {url}\n", encoding="utf-8")

        # Retorna informação mínima
        return Response(
            {"ok": True, "path": str(p), "chunks_created": 1},
            status=status.HTTP_201_CREATED,
        )


class AiCacheStatsView(APIView):
    """Retorna estatísticas do cache."""

    def get(self, request):
        stats = get_cache_stats()
        return Response({"memory_cache": stats, "status": "active"})


class AiCacheCleanupView(APIView):
    """Limpa caches."""

    def post(self, request):
        clear_cache()
        return Response(
            {"message": "Cache limpo com sucesso"},
            status=status.HTTP_200_OK,
        )


class AiHealthCheckView(APIView):
    """Verifica se o serviço Ollama está disponível."""

    def get(self, request):
        try:
            # Teste simples: chama uma completition curta
            test = chat_completion([{"role": "user", "content": "Olá"}])
            healthy = bool(test)
            return Response(
                {"status": "healthy" if healthy else "unhealthy", "ollama_ok": healthy}
            )
        except Exception as e:
            return Response(
                {"status": "unhealthy", "error": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
