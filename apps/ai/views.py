from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .rag import answer, rebuild_index
from .ingestion_web import ingest_url_to_txt
from .serializers import IngestUrlSerializer

class AiAnswerView(APIView):
    def post(self, request):
        q = request.data.get("question", "")
        return Response({"answer": answer(q)})

class AiIngestUrlView(APIView):
    def post(self, request):
        s = IngestUrlSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        url = s.validated_data["url"]
        paths = ingest_url_to_txt(url)
        n = rebuild_index()
        return Response({"ok": True, "chunks_created": len(paths), "total_docs": n}, status=status.HTTP_201_CREATED)
