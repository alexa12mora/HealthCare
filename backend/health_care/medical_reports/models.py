from django.db import models

class Doctor(models.Model):
    codDoctor = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.Name
    
    class Meta:
        db_table = 'Doctor'

class Assistants(models.Model):
    codAssistant = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.Name
    
    class Meta:
        db_table = 'Assistants'

class Patients(models.Model):
    PatientID = models.AutoField(primary_key=True)
    PatientName = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.PatientName
    
    class Meta:
        db_table = 'Patients'

class Banks(models.Model):
    BankID = models.AutoField(primary_key=True)
    BankName = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.BankName
    
    class Meta:
        db_table = 'Banks'

class Insurers(models.Model):
    InsurerID = models.AutoField(primary_key=True)
    InsurerName = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.InsurerName
    
    class Meta:
        db_table = 'Insurers'

class Procedures(models.Model):
    ProcedureID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    ProcedureCost = models.DecimalField(max_digits=10, decimal_places=2)
    InsurerID = models.ForeignKey(Insurers, on_delete=models.CASCADE)
    BankID = models.ForeignKey(Banks, on_delete=models.CASCADE)
    SurgeryType = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.Name
    
    class Meta:
        db_table = 'Procedures'

class AssistantCosts(models.Model):
    CostID = models.AutoField(primary_key=True)
    AssistantType = models.CharField(max_length=100)
    CostAmount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'AssistantCosts'

class OperationCosts(models.Model):
    CostID = models.AutoField(primary_key=True)
    OperationName = models.CharField(max_length=100)
    CostAmount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.OperationName
    
    class Meta:
        db_table = 'OperationCosts'

class ProcedureOperations(models.Model):
    OperationID = models.AutoField(primary_key=True)
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    PatientID = models.ForeignKey(Patients, on_delete=models.CASCADE)
    Date = models.DateField()
    ProcedureID = models.ForeignKey(Procedures, on_delete=models.CASCADE)
    OperationType = models.CharField(max_length=2)
    AssistantCostID = models.ForeignKey(AssistantCosts, on_delete=models.CASCADE)
    OperationCostID = models.ForeignKey(OperationCosts, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ProcedureOperations'

class AccessProfiles(models.Model):
    UserName = models.CharField(max_length=100, primary_key=True)
    Password = models.CharField(max_length=100)
    UserType = models.CharField(max_length=1, choices=[('D', 'Doctor'), ('A', 'Assistant'), ('S', 'Secretary')])
    UserID = models.IntegerField(null=True, blank=True)
    AccessLevel = models.IntegerField()
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.UserName
    
    class Meta:
        db_table = 'AccessProfiles'

class Invoices(models.Model):
    InvoiceNumber = models.AutoField(primary_key=True)
    PaymentDate = models.DateField()
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    PatientID = models.ForeignKey(Patients, on_delete=models.CASCADE)
    PaymentStatus = models.CharField(max_length=20)

    class Meta:
        db_table = 'Invoices'

class AssistantInvoices(models.Model):
    InvoiceAssistantID = models.AutoField(primary_key=True)
    IssuanceDate = models.DateField()
    AssistantID = models.ForeignKey(Assistants, on_delete=models.CASCADE)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'AssistantInvoices'

class AssistantPayments(models.Model):
    OperationID = models.ForeignKey(ProcedureOperations, on_delete=models.CASCADE)
    AssistantID = models.ForeignKey(Assistants, on_delete=models.CASCADE)
    PaidAmount = models.DecimalField(max_digits=10, decimal_places=2)
    PaymentDate = models.DateField()

    class Meta:
        db_table = 'AssistantPayments'
        constraints = [
            models.UniqueConstraint(
                fields=['OperationID', 'AssistantID'],
                name='assistant_payment_pk',
            )
        ]