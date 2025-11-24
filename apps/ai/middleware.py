"""
Middleware para debugging de timeouts e performance.
"""

import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class AIDebugMiddleware(MiddlewareMixin):
    """Middleware para debugar requests da AI."""

    def process_request(self, request):
        # Marca o início do request
        request._start_time = time.time()

        if request.path.startswith("/api/v1/ai/"):
            logger.info(f"[AI] Iniciando request: {request.method} {request.path}")

        return None

    def process_response(self, request, response):
        if hasattr(request, "_start_time"):
            duration = time.time() - request._start_time

            if request.path.startswith("/api/v1/ai/"):
                logger.info(
                    f"[AI] Request completado: {request.method} {request.path} "
                    f"- {response.status_code} - {duration:.2f}s"
                )

                # Log de warning se demorou muito
                if duration > 60:
                    logger.warning(
                        f"[AI] Request lento detectado: {duration:.2f}s para {request.path}"
                    )

        return response

    def process_exception(self, request, exception):
        if hasattr(request, "_start_time"):
            duration = time.time() - request._start_time

            if request.path.startswith("/api/v1/ai/"):
                logger.error(
                    f"[AI] Erro no request: {request.method} {request.path} "
                    f"- {duration:.2f}s - {str(exception)}"
                )

        return None
