from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.patients.views import PatientViewSet, AppointmentViewSet, AdmissionViewSet
from apps.medicaments.views import MedicationViewSet, SupplierViewSet, InventoryBatchViewSet, PrescriptionViewSet, PrescriptionItemViewSet, AdministrationViewSet
from apps.ops.views import ProcessTaskViewSet
from apps.ai.views import AiAnswerView, AiIngestUrlView


router = DefaultRouter()
router.register(r"patients", PatientViewSet)
router.register(r"appointments", AppointmentViewSet)
router.register(r"admissions", AdmissionViewSet)
router.register(r"medications", MedicationViewSet)
router.register(r"suppliers", SupplierViewSet)
router.register(r"inventory-batches", InventoryBatchViewSet)
router.register(r"prescriptions", PrescriptionViewSet)
router.register(r"prescription-items", PrescriptionItemViewSet)
router.register(r"administrations", AdministrationViewSet)
router.register(r"process-tasks", ProcessTaskViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("ai/answer", AiAnswerView.as_view(), name="ai-answer"),
    path("ai/ingest-url", AiIngestUrlView.as_view(), name="ai-ingest-url"),
]
