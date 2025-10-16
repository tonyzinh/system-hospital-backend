from django.db import models

class Medication(models.Model):
    name = models.CharField(max_length=160)
    active_ingredient = models.CharField(max_length=160)
    form = models.CharField(max_length=60)
    strength = models.CharField(max_length=60)
    atc_code = models.CharField(max_length=20, blank=True)

class Supplier(models.Model):
    name = models.CharField(max_length=160)
    cnpj = models.CharField(max_length=32, blank=True)
    contact_json = models.JSONField(default=dict)

class InventoryBatch(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    lot_number = models.CharField(max_length=80)
    expiry_date = models.DateField()
    quantity = models.IntegerField(default=0)
    location = models.CharField(max_length=80, blank=True)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
