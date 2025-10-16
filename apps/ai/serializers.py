from rest_framework import serializers

class IngestUrlSerializer(serializers.Serializer):
    url = serializers.URLField()
