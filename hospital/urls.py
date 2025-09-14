from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('apps.patients.urls')),
    path('api-auth/', include('rest_framework.urls')),
]