from django.contrib import admin
from .models import Patient

class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'cpf', 'birth_date')
    search_fields = ('full_name', 'cpf')

admin.site.register(Patient, PatientAdmin)