from django.db import models

class Hospital(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=80)

class Department(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)

class Patient(models.Model):
    full_name = models.CharField(max_length=160)
    birthdate = models.DateField()
    sex = models.CharField(max_length=1)
    document = models.CharField(max_length=50, blank=True)
    contact_json = models.JSONField(default=dict)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    staff = models.ForeignKey('core.User', on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20, default="scheduled")
    type = models.CharField(max_length=30, default="consult")

class Admission(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    admit_at = models.DateTimeField()
    discharge_at = models.DateTimeField(null=True, blank=True)
    reason = models.CharField(max_length=160, blank=True)
