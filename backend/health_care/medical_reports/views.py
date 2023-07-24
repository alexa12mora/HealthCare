from rest_framework.viewsets import ModelViewSet
from .models import Doctor, Assistants, Patients, Banks, Insurers, Procedures, AssistantCosts, OperationCosts, ProcedureOperations, AccessProfiles, Invoices, AssistantInvoices, AssistantPayments
from .serializers import DoctorSerializer, AssistantsSerializer, PatientsSerializer, BanksSerializer, InsurersSerializer, ProceduresSerializer, AssistantCostsSerializer, OperationCostsSerializer, ProcedureOperationsSerializer, AccessProfilesSerializer, InvoicesSerializer, AssistantInvoicesSerializer, AssistantPaymentsSerializer

class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class AssistantsViewSet(ModelViewSet):
    queryset = Assistants.objects.all()
    serializer_class = AssistantsSerializer

class PatientsViewSet(ModelViewSet):
    queryset = Patients.objects.all()
    serializer_class = PatientsSerializer

class BanksViewSet(ModelViewSet):
    queryset = Banks.objects.all()
    serializer_class = BanksSerializer

class InsurersViewSet(ModelViewSet):
    queryset = Insurers.objects.all()
    serializer_class = InsurersSerializer

class ProceduresViewSet(ModelViewSet):
    queryset = Procedures.objects.all()
    serializer_class = ProceduresSerializer

class AssistantCostsViewSet(ModelViewSet):
    queryset = AssistantCosts.objects.all()
    serializer_class = AssistantCostsSerializer

class OperationCostsViewSet(ModelViewSet):
    queryset = OperationCosts.objects.all()
    serializer_class = OperationCostsSerializer

class ProcedureOperationsViewSet(ModelViewSet):
    queryset = ProcedureOperations.objects.all()
    serializer_class = ProcedureOperationsSerializer

class AccessProfilesViewSet(ModelViewSet):
    queryset = AccessProfiles.objects.all()
    serializer_class = AccessProfilesSerializer

class InvoicesViewSet(ModelViewSet):
    queryset = Invoices.objects.all()
    serializer_class = InvoicesSerializer

class AssistantInvoicesViewSet(ModelViewSet):
    queryset = AssistantInvoices.objects.all()
    serializer_class = AssistantInvoicesSerializer

class AssistantPaymentsViewSet(ModelViewSet):
    queryset = AssistantPayments.objects.all()
    serializer_class = AssistantPaymentsSerializer
