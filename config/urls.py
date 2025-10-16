from django.contrib import admin
from django.urls import path, include
from apps.core.views import healthcheck

urlpatterns = [
    path("", healthcheck),
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
]
