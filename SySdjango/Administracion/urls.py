from django.urls import path
from . import views

urlpatterns = [
    #Rutas main
    path('administracion/empleados/', views.empleados, name='EMPLEADOS'),
    path('administracion/empleados/', views.empleados, name='INVENTARIO'),
    path('administracion/empleados/', views.empleados, name='DISTRIBUIDORES'),
    path('administracion/empleados/', views.empleados, name='VENTAS'),
    path('administracion/empleados/', views.empleados, name='PEDIDOS'),

    ### Rutas CRUD
     #Empleados
    path('administrar/empleado/<int:empleado_id>/', views.editarEmpleado, name="editarEmpleado"),

    #Utilidades Json
    path('listaEmpleados/', views.listaEmpleados, name='listaEmpleados'),
]