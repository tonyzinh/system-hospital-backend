from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ollama_client import chat_completion, OllamaError, clear_cache, get_cache_stats
from .config import get_optimal_settings
from pathlib import Path
import hashlib
import logging
import time


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
    """Endpoint simples de resposta (compatibilidade) - Otimizado."""

    def post(self, request):
        import time

        start_time = time.time()

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

            # Log do início do processamento
            print(
                f"[DEBUG] Processando pergunta: '{q[:50]}...' com timeout {settings['timeout']}s"
            )

            answer = chat_completion(
                [{"role": "user", "content": q}],
                temperature=settings["temperature"],
                max_tokens=settings["max_tokens"],
                timeout=settings["timeout"],
            )

            duration = time.time() - start_time
            print(f"[DEBUG] Resposta gerada em {duration:.2f}s")

            return Response({"answer": answer})

        except OllamaError as e:
            duration = time.time() - start_time
            error_msg = str(e)
            print(f"[ERROR] Falha após {duration:.2f}s: {error_msg}")

            # Retorna erro mais detalhado
            return Response(
                {
                    "detail": error_msg,
                    "duration": f"{duration:.2f}s",
                    "question_length": len(q),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )


class AiAdvancedAnswerView(APIView):
    """Endpoint avançado com retry e logs detalhados."""

    def post(self, request):
        start_time = time.time()
        data = request.data or {}
        question = (data.get("question") or "").strip()
        model = data.get("model")

        if not question:
            return Response(
                {"error": "Pergunta não pode estar vazia"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        print(f"[DEBUG] Advanced: Processando '{question[:50]}...'")

        # Retry logic para melhor resiliência
        max_retries = 2
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                # Otimização baseada na complexidade da pergunta
                settings = get_optimal_settings(question)

                # Aumenta timeout para endpoint avançado
                advanced_timeout = min(settings["timeout"] * 1.5, 180)  # Max 3 min

                print(
                    f"[DEBUG] Advanced: Tentativa {attempt + 1} com timeout {advanced_timeout}s"
                )

                answer = chat_completion(
                    [{"role": "user", "content": question}],
                    model=model,
                    temperature=settings["temperature"],
                    max_tokens=settings["max_tokens"],
                    timeout=advanced_timeout,
                )

                duration = time.time() - start_time
                print(f"[DEBUG] Advanced: Sucesso em {duration:.2f}s")

                return Response({"answer": answer}, status=status.HTTP_200_OK)

            except OllamaError as e:
                last_error = e
                duration = time.time() - start_time
                print(
                    f"[ERROR] Advanced: Tentativa {attempt + 1} falhou em {duration:.2f}s: {str(e)}"
                )

                # Se não for a última tentativa, aguarda um pouco
                if attempt < max_retries:
                    time.sleep(1)
                    continue
                else:
                    break

        # Se chegou aqui, todas as tentativas falharam
        final_duration = time.time() - start_time
        return Response(
            {
                "error": "Erro interno no processamento após múltiplas tentativas",
                "details": str(last_error),
                "duration": f"{final_duration:.2f}s",
                "attempts": max_retries + 1,
            },
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
            # Teste simples e rápido
            test = chat_completion(
                [{"role": "user", "content": "Responda apenas: OK"}],
                timeout=30,  # 30 segundos para health check
            )
            healthy = bool(test and test.strip())

            return Response(
                {
                    "status": "healthy" if healthy else "unhealthy",
                    "ollama_ok": healthy,
                    "response": test[:50] if test else None,
                    "timestamp": time.time(),
                }
            )
        except Exception as e:
            print(f"[ERROR] Health check failed: {str(e)}")
            return Response(
                {
                    "status": "unhealthy",
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "timestamp": time.time(),
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    def post(self, request):
        """Força um teste mais detalhado do Ollama."""
        try:
            start_time = time.time()

            # Teste com pergunta simples
            test = chat_completion(
                [{"role": "user", "content": "Diga apenas 'Funcionando'"}], timeout=30
            )

            duration = time.time() - start_time
            success = bool(test and test.strip())

            if success:
                return Response(
                    {
                        "message": "Ollama testado com sucesso",
                        "status": "healthy",
                        "response": test,
                        "duration": f"{duration:.2f}s",
                    }
                )
            else:
                return Response(
                    {
                        "error": "Resposta vazia do Ollama",
                        "status": "unhealthy",
                        "duration": f"{duration:.2f}s",
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
        except Exception as e:
            duration = time.time() - start_time if "start_time" in locals() else 0
            return Response(
                {"error": f"Erro no teste: {str(e)}", "duration": f"{duration:.2f}s"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
