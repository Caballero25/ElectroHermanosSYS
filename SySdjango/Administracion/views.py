from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.http.response import JsonResponse
from .models import Empleado, HistorialEmpleado

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
            en_servicio = empleado.en_servicio
            #Obtenemos los nuevos datos del empleado
            new_nombres = request.POST['nombres']
            new_apellidos = request.POST['apellidos']
            new_cargo = request.POST['cargo']
            new_direccion = request.POST['direccion']

            #Validamos el formato ecuatoriano de numero telefónico
            if request.POST['telefono'][0] != "0" or request.POST['telefono'][1] != "9":
                print(request.POST['telefono'][0])
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': "El número telefónico debe tener el formato ecuatoriano: 09xxxxxxxx, 10 dígitos numéricos empezados por 09"})

            try:
                longitud_telefono = len(request.POST['telefono'])
                new_telefono = int((request.POST['telefono']))
            except:
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': "Parece que estás tratando de ingresar un texto como número telefónico"})
            new_telefono = "0" + str(new_telefono)
            try:
                new_salario = float((request.POST['salario']))
            except:
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': f"Parece que estás tratando de ingresar un texto o un dato vacío como salario '{request.POST['salario']}'"})

            #Realizamos las validaciones
            if new_nombres == None or new_nombres == "" or new_apellidos == None or new_apellidos == "" or new_cargo == None or new_cargo == "":
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': "Ningún dato puede estar vacío"})
            elif new_telefono == None or new_telefono == "" or new_direccion == None or new_direccion == "" or new_salario == None or new_salario == "" or new_salario == 0:
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': "Ningún dato puede estar vacío"})
            elif  longitud_telefono != 10:
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': f"El número telefónico 0{new_telefono} parece no tener el formato correcto - 10 dígitos numéricos"})
            elif not isinstance(new_salario, (int, float)):
                return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'error': f"El salario que ingresaste {new_salario} no cumple con el requisito numérico"})
            else:
                #Realizamos los cambios
                empleado.nombres = new_nombres
                empleado.apellidos = new_apellidos
                empleado.cargo = new_cargo
                empleado.telefono = new_telefono
                empleado.direccion = new_direccion
                empleado.salario = new_salario
                empleado.save()
                #Guardamos el historial

                #Validamos que datos se cambiaron
                if old_nombres != new_nombres:
                    cambio_nombres = new_nombres
                else:
                    cambio_nombres = "Sin modificaciones"
                if old_apellidos != new_apellidos:
                    cambio_apellidos = new_apellidos
                else:
                    cambio_apellidos = "Sin modificaciones"
                if old_cargo != new_cargo:
                    cambio_cargo = new_cargo
                else:
                    cambio_cargo = "Sin modificaciones"
                if old_telefono != new_telefono:
                    cambio_telefono = new_telefono
                else:
                    cambio_telefono = "Sin modificaciones"
                if old_direccion != new_direccion:
                    cambio_direccion = new_direccion
                else:
                    cambio_direccion = "Sin modificaciones"
                if old_salario != new_salario:
                    cambio_salario = new_salario
                else:
                    cambio_salario = "Sin modificaciones"
                

                nuevoHistorial = HistorialEmpleado.objects.create(
                        #Datos anteriores
                    ant_nombres = old_nombres,
                    ant_apellidos = old_apellidos,
                    ant_cargo = old_cargo,
                    ant_telefono = old_telefono,
                    ant_direccion = old_direccion,
                    ant_salario = old_salario,
                    ant_en_servicio = en_servicio,
                        #Datos actualizados
                    act_nombres = cambio_nombres,
                    act_apellidos = cambio_apellidos,
                    act_cargo = cambio_cargo,
                    act_telefono = cambio_telefono,
                    act_direccion = cambio_direccion,
                    act_salario = new_salario,
                    act_en_servicio = en_servicio,
                        #Responsable de los cambios
                    id_empleado = empleado,
                    administrador = request.user
                )
                nuevoHistorial.save()
                return redirect('editarEmpleado', empleado_id=empleado_id,)
            
    else:
        return render(request, 'error.html', {'error':"Parece que has tratado de acceder a un dato que no es de tu dominio, si crees que es un error contacta a soporte"})


def despedirEmpleado(request, empleado_id):
    empleado = Empleado.objects.get(id=empleado_id)
    idAdministrador = request.user.id
    if empleado.administrador.id == idAdministrador:
        nuevoHistorial = HistorialEmpleado.objects.create(
                        #Datos anteriores
                    ant_nombres = empleado.nombres,
                    ant_apellidos = empleado.apellidos,
                    ant_cargo = empleado.cargo,
                    ant_telefono = empleado.telefono,
                    ant_direccion = empleado.direccion,
                    ant_salario = empleado.salario,
                    ant_en_servicio = empleado.en_servicio,
                        #Datos actualizados
                    act_nombres = "Sin modificaciones",
                    act_apellidos = "Sin modificaciones",
                    act_cargo = "Sin modificaciones",
                    act_telefono = "Sin modificaciones",
                    act_direccion = "Sin modificaciones",
                    act_salario = empleado.salario,
                    act_en_servicio = False,
                        #Responsable de los cambios
                    id_empleado = empleado,
                    administrador = request.user
                )
        nuevoHistorial.save()
        empleado.en_servicio = False  #Se marca al empleado como inactivo
        empleado.save()
        return redirect('editarEmpleado', empleado_id=empleado_id,)
    else:
        return render(request, 'error.html', {'error':"Parece que has tratado de acceder a un dato que no es de tu dominio, si crees que es un error contacta a soporte"})

def recontratarEmpleado(request, empleado_id):
    empleado = Empleado.objects.get(id=empleado_id)
    idAdministrador = request.user.id
    if empleado.administrador.id == idAdministrador:
        nuevoHistorial = HistorialEmpleado.objects.create(
                        #Datos anteriores
                    ant_nombres = empleado.nombres,
                    ant_apellidos = empleado.apellidos,
                    ant_cargo = empleado.cargo,
                    ant_telefono = empleado.telefono,
                    ant_direccion = empleado.direccion,
                    ant_salario = empleado.salario,
                    ant_en_servicio = empleado.en_servicio,
                        #Datos actualizados
                    act_nombres = "Sin modificaciones",
                    act_apellidos = "Sin modificaciones",
                    act_cargo = "Sin modificaciones",
                    act_telefono = "Sin modificaciones",
                    act_direccion = "Sin modificaciones",
                    act_salario = empleado.salario,
                    act_en_servicio = True,
                        #Responsable de los cambios
                    id_empleado = empleado,
                    administrador = request.user
                )
        nuevoHistorial.save()
        empleado.en_servicio = True  #Se marca al empleado como activo
        empleado.save()
        return redirect('editarEmpleado', empleado_id=empleado_id,)
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

#Nomina........
def getNomina(request, empleado_id):
    json = {'prueba': empleado_id}
    return render(request, '03-nominaEmpleado.html')