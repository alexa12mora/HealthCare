from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

class MedicoAdmin(admin.ModelAdmin):
    list_display = ['codMedico', 'Nombre', 'correo']

class SecretariaAdmin(admin.ModelAdmin):
    list_display = ['codSecretaria', 'Nombre', 'correo']

admin.site.register(Medico, MedicoAdmin)
admin.site.register(Secretaria, SecretariaAdmin)

admin.site.unregister(Group)  
admin.site.add_action(Group)  


admin.site.register(CostosPorAsistente)
admin.site.register(Asistentes)
admin.site.register(Emisor)
admin.site.register(Aseguradoras)
admin.site.register(CostosDeOperaciones)
admin.site.register(servicios)
admin.site.register(Facturas)
admin.site.register(FacturasAsistentes)
admin.site.register(PagosAsistentes)

