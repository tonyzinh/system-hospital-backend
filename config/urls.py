from django.contrib import admin
from django.urls import path, include
from apps.core.views import healthcheck
from apps.ai.views import AiChatView, AiAnswerView

urlpatterns = [
    path("", healthcheck),
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("ai/chat", AiChatView.as_view(), name="ai-chat"),
    path("ai/answer", AiAnswerView.as_view(), name="ai-answer"),
]
