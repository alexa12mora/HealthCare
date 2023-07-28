from django.contrib import admin
from .models import Medico, CostosPorAsistente, Asistentes, Emisor, Aseguradoras, CostosDeOperaciones, servicios, Facturas, FacturasAsistentes, PagosAsistentes, PerfilesDeAcceso

admin.site.register(Medico)
admin.site.register(CostosPorAsistente)
admin.site.register(Asistentes)
admin.site.register(Emisor)
admin.site.register(Aseguradoras)
admin.site.register(CostosDeOperaciones)
admin.site.register(servicios)
admin.site.register(Facturas)
admin.site.register(FacturasAsistentes)
admin.site.register(PagosAsistentes)
admin.site.register(PerfilesDeAcceso)
