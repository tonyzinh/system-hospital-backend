from django.contrib import admin
from .models import User, AuditLog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","username","email","role","is_staff","is_superuser","date_joined")
    search_fields = ("username","email","role")

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id","user","action","entity","entity_id","timestamp")
    list_filter = ("action","entity")
    search_fields = ("entity","entity_id")
