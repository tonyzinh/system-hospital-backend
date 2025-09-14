from django.urls import path
from .views import PatientListCreateAPIView

urlpatterns = [
    path('patients/', PatientListCreateAPIView.as_view(), name='patient-list-create'),
]