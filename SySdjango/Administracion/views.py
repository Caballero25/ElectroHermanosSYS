from django.shortcuts import render
from django.core.serializers import serialize
from django.http.response import JsonResponse
from .models import Empleado

# Create your views here.

def empleados(request):
    idAdministrador = request.user.id
    empleados = Empleado.objects.filter(administrador=idAdministrador)
    return render(request, '01-empleados.html', {'empleados':empleados}) 

def editarEmpleado(request, empleado_id):
    empleado = Empleado.objects.get(id=empleado_id)
    idAdministrador = request.user.id
    if empleado.administrador.id == idAdministrador:
        print(empleado)
        return render(request, '02-editarEmpleado.html', {'empleado': empleado})
    else:
        return render(request, 'error.html', {'error':"Parece que has tratado de acceder a un dato que no es de tu dominio, si crees que es un error contacta a soporte"})

def listaEmpleados(request):
    idAdministrador = request.user.id
    empleados = Empleado.objects.filter(administrador=idAdministrador)
    empleados_data = []

    for empleado in empleados:
        empleado_data = {
            "model": "Administracion.empleado",
            "pk": empleado.pk,
            "fields": {
                "nombres": empleado.nombres,
                "apellidos": empleado.apellidos,
                "cargo": empleado.cargo,
                "telefono": empleado.telefono,
                "direccion": empleado.direccion,
                "fecha_ingreso": empleado.fecha_ingreso.isoformat(),
                "salario": empleado.salario,
                "activo": empleado.en_servicio,
            }
        }
        empleados_data.append(empleado_data)

    return JsonResponse(empleados_data, safe=False)