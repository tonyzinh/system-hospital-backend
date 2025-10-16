from rest_framework import viewsets
from .models import ProcessTask
from .serializers import ProcessTaskSerializer

class ProcessTaskViewSet(viewsets.ModelViewSet):
    queryset = ProcessTask.objects.all().order_by("-priority_score")
    serializer_class = ProcessTaskSerializer
