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
    path('despedir/empleado/<int:empleado_id>/', views.despedirEmpleado, name="despedirEmpleado"),
    path('recontratar/empleado/<int:empleado_id>/', views.recontratarEmpleado, name="recontratarEmpleado"),
     #Nomina
    path('nomina/empleado/<int:empleado_id>/', views.getNomina, name='nominaEmpleado'),

    #Utilidades Json
    path('listaEmpleados/', views.listaEmpleados, name='listaEmpleados'),
]