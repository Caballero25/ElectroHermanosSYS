from django.contrib import admin
from .models import Empleado, HistorialEmpleado, DatosTemporalesNomina

# Register your models here.
admin.site.register(Empleado)
admin.site.register(HistorialEmpleado)
admin.site.register(DatosTemporalesNomina)
