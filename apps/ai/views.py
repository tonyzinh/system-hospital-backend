from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ollama_client import chat_completion, OllamaError


class AiChatView(APIView):
    """
    POST /api/v1/ai/chat
    body:
    {
      "question": "texto do usuário",
      "history": [{"role":"user","content":"..."}, {"role":"assistant","content":"..."}],  # opcional
      "model": "llama3.1"    # opcional
    }
    """

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

        try:
            answer = chat_completion(messages, model=model)
            return Response({"answer": answer})
        except OllamaError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class AiAnswerView(APIView):
    """
    POST /api/v1/ai/answer
    body: { "question": "..." }
    """

    def post(self, request):
        data = request.data or {}
        q = (data.get("question") or "").strip()
        if not q:
            return Response(
                {"detail": "question é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            answer = chat_completion([{"role": "user", "content": q}])
            return Response({"answer": answer})
        except OllamaError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
