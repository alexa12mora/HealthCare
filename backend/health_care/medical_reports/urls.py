from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'doctors', views.DoctorViewSet, basename="doctors")
router.register(r'assistants', views.AssistantsViewSet, basename="assistants")
router.register(r'patients', views.PatientsViewSet, basename="patients")
router.register(r'banks', views.BanksViewSet, basename="banks")
router.register(r'insurers', views.InsurersViewSet, basename="insurers")
router.register(r'procedures', views.ProceduresViewSet, basename="procedures")
router.register(r'assistant_costs', views.AssistantCostsViewSet, basename="assistant_costs")
router.register(r'operation_costs', views.OperationCostsViewSet, basename="operation_costs")
router.register(r'procedure_operations', views.ProcedureOperationsViewSet, basename="procedure_operations")
router.register(r'access_profiles', views.AccessProfilesViewSet, basename="access_profiles")
router.register(r'invoices', views.InvoicesViewSet, basename="invoices")
router.register(r'assistant_invoices', views.AssistantInvoicesViewSet, basename="assistant_invoices")
router.register(r'assistant_payments', views.AssistantPaymentsViewSet, basename="assistant_payments")

urlpatterns = [
    path('', include(router.urls)),
    # Add other URL patterns here if needed
]

