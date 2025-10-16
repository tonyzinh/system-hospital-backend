from django.contrib import admin
from .models import Medication, Supplier, InventoryBatch
from .models_rx import Prescription, PrescriptionItem, Administration

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active_ingredient", "form", "strength", "atc_code")
    search_fields = ("name", "active_ingredient", "atc_code")

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cnpj")
    search_fields = ("name", "cnpj")

@admin.register(InventoryBatch)
class InventoryBatchAdmin(admin.ModelAdmin):
    list_display = ("id", "medication", "supplier", "lot_number", "expiry_date", "quantity")
    list_filter = ("expiry_date",)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "prescriber", "created_at", "status")
    list_filter = ("status",)

@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ("id", "prescription", "medication", "dose", "frequency", "route", "duration_days")

@admin.register(Administration)
class AdministrationAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "medication", "staff", "timestamp", "dose_given", "adverse_event_flag")
    list_filter = ("adverse_event_flag",)
