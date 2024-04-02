from django.db import models
from django.contrib.auth.models import User 

class Medico(models.Model):
    codMedico = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)

    def __str__(self):
        return self.Nombre
    
    
class Secretaria(models.Model):
    codSecretaria = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre

class CostosPorAsistente(models.Model):
    CodCostoPorAsistente = models.AutoField(primary_key=True)
    TipoAsistente = models.CharField(max_length=100)
    MontoCosto = models.DecimalField(max_digits=10, decimal_places=1)
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
    MontoCosto = models.DecimalField(max_digits=10, decimal_places=1)
    codMedico = models.ForeignKey(User, on_delete=models.CASCADE)  # Agrega ForeignKey a User

    def __str__(self):
        return self.NombreOperacion
     
class servicios(models.Model):
    CodProcedimiento = models.AutoField(primary_key=True)
    Fecha = models.DateField()
    NombrePaciente = models.CharField(max_length=100)
    MontoTotal = models.DecimalField(max_digits=10, decimal_places=1)
    MedioPago = models.CharField(max_length=20)
    CodAseguradora = models.ForeignKey(Aseguradoras, on_delete=models.CASCADE, blank=True, null=True)
    CodHospital = models.ForeignKey(Hospitales, on_delete=models.CASCADE,default=1)
    CodBanco = models.ForeignKey(Emisor, on_delete=models.CASCADE)
    EstadoPago = models.CharField(max_length=20)
    codMedico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    numFactura = models.CharField(max_length=20)
    CodCostoOperacion = models.ForeignKey(CostosDeOperaciones, on_delete=models.CASCADE,default=1)
    EstadoCierre = models.BooleanField(default=False)
    EstadoFactura = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Procedimiento {self.CodProcedimiento}"
    
   
class Asistentes(models.Model):
    CodAsistente = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    CodCostoPorAsistente = models.ForeignKey(CostosPorAsistente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(servicios, on_delete=models.CASCADE)
    monto =  models.DecimalField(default=0.0, max_digits=10, decimal_places=1)

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
       
class Reporte(models.Model):
    CodReporte = models.AutoField(primary_key=True)
    FechaReporte = models.DateField()
    Servicios = models.ManyToManyField(servicios)  # Relación ManyToMany con servicios
    Medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    Asistente = models.ForeignKey(Asistentes, on_delete=models.CASCADE)
    estado = models.BooleanField(default=False)
    EstadoCierre = models.BooleanField(default=False)
    def __str__(self):
        return f"Reporte {self.CodReporte}"

class FacturasAsistentes(models.Model):
    NumFacturaAsistente = models.AutoField(primary_key=True)
    FechaEmision = models.DateField(null=True, blank=True)
    CodReporte = models.ForeignKey(Reporte, on_delete=models.CASCADE) 
    descFactura = models.CharField(null=True,max_length=100,blank=True)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return f"FacturaAsistente {self.NumFacturaAsistente}"


class PagosAsistentes(models.Model):
    CodReporte = models.ForeignKey(Reporte, on_delete=models.CASCADE) 
    CodAsistente = models.ForeignKey(Asistentes, on_delete=models.CASCADE)
    MontoPagado = models.DecimalField(max_digits=10, decimal_places=1)
    FechaPago = models.DateField()
    descFactura = models.CharField(null=True,max_length=100,blank=True)
    def __str__(self):
        return f"CodReporte {self.CodReporte}"

class Cobros(models.Model):
    NumCobro = models.AutoField(primary_key=True)
    FechaCreacion = models.DateField(null=True, blank=True)
    FechaPago = models.DateField(null=True, blank=True)
    NombreDelCliente = models.CharField(max_length=100)
    NombrepacienteAsociado = models.CharField(max_length=100)
    MontoCobrar = models.DecimalField(max_digits=10, decimal_places=1)
    TipoCirugia = models.CharField(max_length=100)
    Medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    numReferenciaBanco = models.CharField(max_length=30,blank=True)
    Estado = models.BooleanField(default=False)
    def __str__(self):
        return f"Factura {self.NumCobro}"
    
    
    
class ReporteServiciosPorDeuda(models.Model):
    CodReporte = models.AutoField(primary_key=True)
    FechaReporte = models.DateField()
    Medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    Asistente = models.ForeignKey(Asistentes, on_delete=models.CASCADE)
    Reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE)
    MontoDiferencia = models.DecimalField(max_digits=10, decimal_places=1)
    def __str__(self):
        return f"ReporteServiciosPorDeuda {self.CodReporte}" 