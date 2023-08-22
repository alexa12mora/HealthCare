from django.db import models
from django.contrib.auth.models import User 

class Medico(models.Model):
    codMedico = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)

    def __str__(self):
        return self.Nombre
    
class Secreataria(models.Model):
    codSecretaria = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)

    def __str__(self):
        return self.Nombre

class CostosPorAsistente(models.Model):
    CodCostoPorAsistente = models.AutoField(primary_key=True)
    TipoAsistente = models.CharField(max_length=100)
    MontoCosto = models.DecimalField(max_digits=10, decimal_places=2)
    codMedico = models.ForeignKey(User, on_delete=models.CASCADE)  # Agrega ForeignKey a User

    def __str__(self):
        return self.TipoAsistente
    
class Emisor(models.Model):
    CodBanco = models.AutoField(primary_key=True)
    NombreBanco = models.CharField(max_length=100)
    codMedico = models.ForeignKey(User, on_delete=models.CASCADE)  # Agrega ForeignKey a User

    def __str__(self):
        return self.NombreBanco

class Aseguradoras(models.Model):
    CodAseguradora = models.AutoField(primary_key=True)
    NombreAseguradora = models.CharField(max_length=100)
    codMedico = models.ForeignKey(User, on_delete=models.CASCADE)  # Agrega ForeignKey a User

    def __str__(self):
        return self.NombreAseguradora

class Hospitales(models.Model):
    CodHospital = models.AutoField(primary_key=True)
    NombreHospital = models.CharField(max_length=100)
    codMedico = models.ForeignKey(User, on_delete=models.CASCADE)  # Agrega ForeignKey a User

    def __str__(self):
        return self.NombreHospital
        
class CostosDeOperaciones(models.Model):
    CodCostoOperacion = models.AutoField(primary_key=True)
    NombreOperacion = models.CharField(max_length=100)
    MontoCosto = models.DecimalField(max_digits=10, decimal_places=2)
    codMedico = models.ForeignKey(User, on_delete=models.CASCADE)  # Agrega ForeignKey a User

    def __str__(self):
        return self.NombreOperacion
     
class servicios(models.Model):
    CodProcedimiento = models.AutoField(primary_key=True)
    Fecha = models.DateField()
    NombrePaciente = models.CharField(max_length=100)
    MontoTotal = models.DecimalField(max_digits=10, decimal_places=2)
    MedioPago = models.CharField(max_length=20)
    CodAseguradora = models.ForeignKey(Aseguradoras, on_delete=models.CASCADE)
    CodHospital = models.ForeignKey(Hospitales, on_delete=models.CASCADE,default=1)
    CodBanco = models.ForeignKey(Emisor, on_delete=models.CASCADE)
    EstadoPago = models.CharField(max_length=20)
    codMedico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    numFactura = models.CharField(max_length=20)
    CodCostoOperacion = models.ForeignKey(CostosDeOperaciones, on_delete=models.CASCADE,default=1)
    
    def __str__(self):
        return f"Procedimiento {self.CodProcedimiento}"
    
   
class Asistentes(models.Model):
    CodAsistente = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    CodCostoPorAsistente = models.ForeignKey(CostosPorAsistente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(servicios, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre

    
class Facturas(models.Model):
    NumFactura = models.AutoField(primary_key=True)
    FechaPago = models.DateField(null=True, blank=True)
    NumeroFactura = models.CharField(max_length=100,blank=True)
    CodProcedimiento = models.ForeignKey(servicios, on_delete=models.CASCADE)
    estado = models.BooleanField(default=False)
    def __str__(self):
        return f"Factura {self.NumFactura}"


class FacturasAsistentes(models.Model):
    NumFacturaAsistente = models.AutoField(primary_key=True)
    FechaEmision = models.DateField(null=True, blank=True)
    CodAsistente = models.ForeignKey(Asistentes, on_delete=models.CASCADE)
    descFactura = models.CharField(null=True,max_length=100,blank=True)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return f"FacturaAsistente {self.NumFacturaAsistente}"


class PagosAsistentes(models.Model):
    CodOperacion = models.ForeignKey(servicios, on_delete=models.CASCADE)
    CodAsistente = models.ForeignKey(Asistentes, on_delete=models.CASCADE)
    MontoPagado = models.DecimalField(max_digits=10, decimal_places=2)
    FechaPago = models.DateField()

    def __str__(self):
        return f"PagoAsistente {self.CodOperacion} - {self.CodAsistente}"

