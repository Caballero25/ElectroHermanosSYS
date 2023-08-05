from django.urls import path
from . import views

urlpatterns = [
    path('administracion/empleados/', views.empleados, name='EMPLEADOS'),
    path('administracion/empleados/', views.empleados, name='INVENTARIO'),
    path('administracion/empleados/', views.empleados, name='DISTRIBUIDORES'),
    path('administracion/empleados/', views.empleados, name='VENTAS'),
    path('administracion/empleados/', views.empleados, name='PEDIDOS'),

    #Utilidades Json
    path('listaEmpleados/', views.listaEmpleados, name='listaEmpleados'),
]