from django.shortcuts import render
from django.core.serializers import serialize
from django.http.response import JsonResponse
from .models import Empleado

# Create your views here.

def empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados.html', {'empleados':empleados}) 


def listaEmpleados(_request):
    empleados = Empleado.objects.all()
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
            }
        }
        empleados_data.append(empleado_data)

    return JsonResponse(empleados_data, safe=False)