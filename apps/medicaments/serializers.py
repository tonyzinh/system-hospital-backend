from rest_framework import serializers
from .models import Medication, Supplier, InventoryBatch
from .models_rx import Prescription, PrescriptionItem, Administration

class MedicationSerializer(serializers.ModelSerializer):
    class Meta: model = Medication; fields = "__all__"

class SupplierSerializer(serializers.ModelSerializer):
    class Meta: model = Supplier; fields = "__all__"

class InventoryBatchSerializer(serializers.ModelSerializer):
    class Meta: model = InventoryBatch; fields = "__all__"

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta: model = Prescription; fields = "__all__"

class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta: model = PrescriptionItem; fields = "__all__"

class AdministrationSerializer(serializers.ModelSerializer):
    class Meta: model = Administration; fields = "__all__"
