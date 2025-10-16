from django.db import models

class ProcessTask(models.Model):
    entity_type = models.CharField(max_length=40)
    entity_id = models.CharField(max_length=64)
    name = models.CharField(max_length=120)
    status = models.CharField(max_length=20, default="pending")
    sla_minutes = models.IntegerField(default=60)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    priority_score = models.FloatField(default=0.0)

    class Meta:
        indexes = [models.Index(fields=["status","priority_score"])]
