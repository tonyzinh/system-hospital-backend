from django.db import models
from .models import Medication

class Prescription(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    prescriber = models.ForeignKey('core.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="active")

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dose = models.CharField(max_length=60)
    frequency = models.CharField(max_length=60)
    route = models.CharField(max_length=40)
    duration_days = models.IntegerField(default=0)
    notes = models.TextField(blank=True)

class Administration(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    staff = models.ForeignKey('core.User', on_delete=models.CASCADE)
    prescription_item = models.ForeignKey(PrescriptionItem, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    dose_given = models.CharField(max_length=60)
    adverse_event_flag = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
