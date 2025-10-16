from django.contrib import admin
from .models import Hospital, Department, Patient, Appointment, Admission

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city")
    search_fields = ("name", "city")

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "hospital")
    list_filter = ("hospital",)
    search_fields = ("name",)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "birthdate", "sex")
    search_fields = ("full_name", "document")

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "staff", "scheduled_at", "status", "type")
    list_filter = ("status", "type")

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "department", "admit_at", "discharge_at")
    list_filter = ("department",)
