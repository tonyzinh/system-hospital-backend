from django.contrib import admin
from .models import ProcessTask

@admin.register(ProcessTask)
class ProcessTaskAdmin(admin.ModelAdmin):
    list_display = ("id","entity_type","entity_id","status","sla_minutes","priority_score","started_at","completed_at")
    list_filter = ("status",)
    search_fields = ("entity_type","entity_id","name")
