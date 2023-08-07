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
        if request.method == 'GET':
            return render(request, '02-editarEmpleado.html', {'empleado': empleado})
        else:
            #Obtenemos los datos anteriores del empleado:
            old_nombres = empleado.nombres
            old_apellidos = empleado.apellidos
            old_cargo = empleado.cargo
            old_telefono = empleado.telefono
            old_direccion = empleado.direccion
            old_salario = empleado.salario
            #Obtenemos los nuevos datos del empleado
            new_nombres = request.POST['nombres']
            new_apellidos = request.POST['apellidos']
            new_cargo = request.POST['cargo']
            new_direccion = request.POST['direccion']
            print(request.POST['telefono'])
            print(type(request.POST['telefono']))
            print(len(request.POST['telefono']))

            try:
                longitud_telefono = len(request.POST['telefono'])
                new_telefono = int((request.POST['telefono']))
            except:
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': "Parece que estás tratando de ingresar un texto como número telefónico"})

            try:
                new_salario = float((request.POST['salario']))
            except:
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': f"Parece que estás tratando de ingresar un texto como salario '{request.POST['salario']}'"})

            #Realizamos las validaciones
            if new_nombres == None or new_nombres == "" or new_apellidos == None or new_apellidos == "" or new_cargo == None or new_cargo == "":
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': "Ningún dato puede estar vacío"})
            elif new_telefono == None or new_telefono == "" or new_direccion == None or new_direccion == "" or new_salario == None or new_salario == "" or new_salario == 0:
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': "Ningún dato puede estar vacío"})
            elif  longitud_telefono != 10:
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': f"El número telefónico {new_telefono} parece no tener el formato correcto - 10 dijitos numéricos"})
            elif not isinstance(new_salario, (int, float)):
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': f"El salario que ingresaste {new_salario} no cumple con el requisito numérico"})

            #Realizamos los cambios
            empleado.nombres = new_nombres
            empleado.apellidos = new_apellidos
            empleado.cargo = new_cargo
            empleado.telefono = new_telefono
            empleado.direccion = new_direccion
            empleado.salario = new_salario
            return JsonResponse({old_salario: new_salario})
            
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