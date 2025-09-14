from django.http import HttpResponse

def home_view(request):
    return HttpResponse("<h1>Bem-vindo à API do Sistema Hospitalar</h1>")