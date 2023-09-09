from django.urls import path
from . import views

urlpatterns = [
    #Rutas main
    path('administracion/empleados/', views.empleados, name='EMPLEADOS'),
    path('administracion/addempleados/', views.contratar, name='addEmpleados'),

    ### Rutas CRUD
     #Empleados
    path('administrar/empleado/<int:empleado_cedula>/', views.editarEmpleado, name="editarEmpleado"),
    path('despedir/empleado/<int:empleado_id>/', views.despedirEmpleado, name="despedirEmpleado"),
    path('recontratar/empleado/<int:empleado_id>/', views.recontratarEmpleado, name="recontratarEmpleado"),
     #Nomina
    path('nomina/empleado/<int:empleado_cedula>/', views.getNomina, name='nominaEmpleado'),

    #Utilidades Json
    path('listaEmpleados/', views.listaEmpleados, name='listaEmpleados'),
    path('$2a$12$CxlKpCO0VnHK7GGPQCPuE.rEAtxaDanVZuuQwc6sKCSLSNbo4D53u/', views.pagoNominaMensual, name='nominapago'),
]