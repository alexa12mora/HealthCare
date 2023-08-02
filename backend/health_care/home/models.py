from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Zona(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True

class Dominio(DomainMixin):
    pass

class Medico(models.Model):
    codMedico = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)

    def __str__(self):
        return self.Nombre

class CostosPorAsistente(models.Model):
    CodCostoPorAsistente = models.AutoField(primary_key=True)
    TipoAsistente = models.CharField(max_length=100)
    MontoCosto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.TipoAsistente

class Emisor(models.Model):
    CodBanco = models.AutoField(primary_key=True)
    NombreBanco = models.CharField(max_length=100)

    def __str__(self):
        return self.NombreBanco

class Aseguradoras(models.Model):
    CodAseguradora = models.AutoField(primary_key=True)
    NombreAseguradora = models.CharField(max_length=100)

    def __str__(self):
        return self.NombreAseguradora

class Hospitales(models.Model):
    CodHospital = models.AutoField(primary_key=True)
    NombreHospital = models.CharField(max_length=100)

    def __str__(self):
        return self.NombreHospital
        
class CostosDeOperaciones(models.Model):
    CodCostoOperacion = models.AutoField(primary_key=True)
    NombreOperacion = models.CharField(max_length=100)
    MontoCosto = models.DecimalField(max_digits=10, decimal_places=2)

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
    DescripcionProcedimiento = models.CharField(max_length=200)
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
    FechaPago = models.DateField()
    CodProcedimiento = models.ForeignKey(servicios, on_delete=models.CASCADE)
    def __str__(self):
        return f"Factura {self.NumFactura}"


class FacturasAsistentes(models.Model):
    NumFacturaAsistente = models.AutoField(primary_key=True)
    FechaEmision = models.DateField()
    CodAsistente = models.ForeignKey(Asistentes, on_delete=models.CASCADE)
    CodProcedimiento = models.ForeignKey(servicios, on_delete=models.CASCADE)  # En lugar de CodAsistente
    descFactura = models.CharField(max_length=100)

    def __str__(self):
        return f"FacturaAsistente {self.NumFacturaAsistente}"


class PagosAsistentes(models.Model):
    CodOperacion = models.ForeignKey(servicios, on_delete=models.CASCADE)
    CodAsistente = models.ForeignKey(Asistentes, on_delete=models.CASCADE)
    MontoPagado = models.DecimalField(max_digits=10, decimal_places=2)
    FechaPago = models.DateField()

    def __str__(self):
        return f"PagoAsistente {self.CodOperacion} - {self.CodAsistente}"


# class PerfilesDeAcceso(models.Model):
#     NombreUsuario = models.CharField(max_length=100, primary_key=True)
#     Password = models.CharField(max_length=100)
#     TipoUsuario = models.CharField(max_length=1, choices=[('M', 'Medico'), ('A', 'Asistente'), ('S', 'Otro')])
#     NivelDeAcceso = models.IntegerField()

#     def __str__(self):
#         return self.NombreUsuario
