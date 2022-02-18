from io import UnsupportedOperation
from django.contrib import admin

from .models import *

class CertificadoAdmin(admin.ModelAdmin):
    fields = ['usuario', 'curso']

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Dependencia)
admin.site.register(Curso)
admin.site.register(Sesion)
admin.site.register(Plantilla)
admin.site.register(Certificado, CertificadoAdmin)
admin.site.register(Usuario_Curso)
admin.site.register(Encuesta)
