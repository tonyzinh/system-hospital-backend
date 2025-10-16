from rest_framework import viewsets
from .models import Medication, Supplier, InventoryBatch
from .models_rx import Prescription, PrescriptionItem, Administration
from .serializers import *

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all().order_by("name")
    serializer_class = MedicationSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by("name")
    serializer_class = SupplierSerializer

class InventoryBatchViewSet(viewsets.ModelViewSet):
    queryset = InventoryBatch.objects.all().order_by("expiry_date")
    serializer_class = InventoryBatchSerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().order_by("-created_at")
    serializer_class = PrescriptionSerializer

class PrescriptionItemViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer

class AdministrationViewSet(viewsets.ModelViewSet):
    queryset = Administration.objects.all().order_by("-timestamp")
    serializer_class = AdministrationSerializer
