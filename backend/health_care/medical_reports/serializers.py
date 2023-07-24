from rest_framework import serializers
from .models import Doctor, Assistants, Patients, Banks, Insurers, Procedures, AssistantCosts, OperationCosts, ProcedureOperations, AccessProfiles, Invoices, AssistantInvoices, AssistantPayments

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class AssistantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistants
        fields = '__all__'

class PatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = '__all__'

class BanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = '__all__'

class InsurersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurers
        fields = '__all__'

class ProceduresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedures
        fields = '__all__'

class AssistantCostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistantCosts
        fields = '__all__'

class OperationCostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationCosts
        fields = '__all__'

class ProcedureOperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureOperations
        fields = '__all__'

class AccessProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessProfiles
        fields = '__all__'

class InvoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoices
        fields = '__all__'

class AssistantInvoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistantInvoices
        fields = '__all__'

class AssistantPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistantPayments
        fields = '__all__'
