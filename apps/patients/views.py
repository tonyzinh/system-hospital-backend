from rest_framework import viewsets
from .models import Patient, Appointment, Admission
from .serializers import PatientSerializer, AppointmentSerializer, AdmissionSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("full_name")
    serializer_class = PatientSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by("-scheduled_at")
    serializer_class = AppointmentSerializer

class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all().order_by("-admit_at")
    serializer_class = AdmissionSerializer
