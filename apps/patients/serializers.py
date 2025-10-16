from rest_framework import serializers
from .models import Patient, Appointment, Admission

class PatientSerializer(serializers.ModelSerializer):
    class Meta: model = Patient; fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta: model = Appointment; fields = "__all__"

class AdmissionSerializer(serializers.ModelSerializer):
    class Meta: model = Admission; fields = "__all__"
