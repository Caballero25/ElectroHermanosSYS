from django.contrib import admin
from .models import Empleado, Inventario, Proveedores, HistorialCompras, HistorialVentas

# Register your models here.
admin.site.register(Empleado)
admin.site.register(Inventario)
admin.site.register(Proveedores)
admin.site.register(HistorialCompras)
admin.site.register(HistorialVentas)