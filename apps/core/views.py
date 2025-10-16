from django.http import JsonResponse

def healthcheck(_request):
    return JsonResponse({"status": "ok", "service": "system-hospital-backend"})