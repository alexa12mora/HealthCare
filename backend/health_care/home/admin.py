from django.contrib import admin
from .models import *

admin.site.register(Zona)
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

