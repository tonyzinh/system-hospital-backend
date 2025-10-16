from rest_framework import serializers
from .models import ProcessTask


class ProcessTaskSerializer(serializers.ModelSerializer):
    class Meta: model = ProcessTask; fields = "__all__"
