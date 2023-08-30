from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from .models import Empleado, HistorialEmpleado, DatosTemporalesNomina, ConstanciaPago
from apscheduler.schedulers.blocking import BlockingScheduler

# Create your views here.

def empleados(request):
    idAdministrador = request.user.id
    empleados = Empleado.objects.filter(administrador=idAdministrador)
    return render(request, '01-empleados.html', {'empleados':empleados}) 

def editarEmpleado(request, empleado_cedula):
    empleado = Empleado.objects.get(cedula=empleado_cedula)
    idAdministrador = request.user.id
    if empleado.administrador.id == idAdministrador:
        historialEmpleado = HistorialEmpleado.objects.filter(id_empleado = empleado.id)
        if request.method == 'GET':
            return render(request, '02-editarEmpleado.html', {'empleado': empleado, 'historial': historialEmpleado})
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
                    cambio_salario = old_salario
                

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
                    act_salario = cambio_salario,
                    act_en_servicio = en_servicio,
                        #Responsable de los cambios
                    id_empleado = empleado,
                    administrador = request.user
                )
                nuevoHistorial.save()
                if old_salario != new_salario:
                    return redirect('nominaEmpleado', empleado_cedula=empleado_cedula,)
                else:
                    return redirect('editarEmpleado', empleado_cedula=empleado_cedula,)
            
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
        return redirect('editarEmpleado', empleado_cedula=empleado.cedula)
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
        return redirect('editarEmpleado', empleado_cedula=empleado.cedula)
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
            "cedula": empleado.cedula,
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
def getNomina(request, empleado_cedula):
    empleado = Empleado.objects.get(cedula=empleado_cedula)
    idAdministrador = request.user.id
    if empleado.administrador.id == idAdministrador:
        nominaTemporal = DatosTemporalesNomina.objects.get(id_empleado=empleado.id)
        #Valores base salario
        v_dia_base = round(empleado.salario / 30, 2)
        v_hora_base = round(v_dia_base / 8, 2)
        v_hora_normal_ext = round(((v_hora_base * 25) / 100) + v_hora_base , 2)
        v_hora_nocturna = round(((v_hora_base * 35) / 100) + v_hora_base, 2)
        v_hora_dominical = round(((v_hora_base * 110) / 100 ) + v_hora_base, 2)
        v_hora_dominical_nocturno = round(((v_hora_base * 150) / 100 ) + v_hora_base, 2)
        v_hora_ext_nocturna = round(((v_hora_base * 75) / 100) + v_hora_base, 2)
        valores_base = {
            'v_dia_base': v_dia_base,
            'v_hora_base': v_hora_base,
            'v_hora_nocturna': v_hora_nocturna,
            'v_hora_dominical': v_hora_dominical,
            'v_hora_dominical_nocturno': v_hora_dominical_nocturno
        }

        if request.method == 'GET':
            if nominaTemporal.pago_mes == 0:
                nominaTemporal.pago_mes = empleado.salario
                nominaTemporal.save()
            else:
                nominaTemporal.pago_mes = nominaTemporal.pago_mes
            return render(request, '03-nominaEmpleado.html', {'empleado': empleado, 'nomina': nominaTemporal, 'valoresBase': valores_base, 'pagoActual': 100})
        if request.method == 'POST':
            if 'busquedaCedula' in request.POST:
                empleado_cedula = request.POST['busquedaCedula']
                return redirect('nominaEmpleado', empleado_cedula=empleado_cedula,)
            Nuevo_Salario = 0
            try:
                dias_trabajados = int(request.POST['dias_habiles_mes'])
                hrs_normales_trabajadas = int(request.POST['hrs_norms_dia'])
                hrs_nocturnas_trabajadas = int(request.POST['hrs_nctna_mes'])
                hrs_extras_nocturnas = int(request.POST['h_ext_nctna_mes'])
                hrs_dominical_trabajadas = int(request.POST['hrs_domcal_mes'])
                hrs_dominical_nocturnas_trabajadas = int(request.POST['hrs_domcal_noctna_mes'])
                hrs_semanales_contrato = int(request.POST['hrs_semanales'])
                hrs_extras_normales = int(request.POST['hrs_norms_extras'])
            except:
                return render(request, 'error.html', {'error':"Parece que has introducido letras o datos vacíos en la nómina, por favor reectifica, si crees que se trata de un error por favor comunicate con soporte."})
            #Actualizamos los datos antiguos de nómina
            nominaTemporal.dias_trabajados = dias_trabajados
            nominaTemporal.hrs_normales_trabajadas = hrs_normales_trabajadas
            nominaTemporal.hrs_nocturnas_trabajadas = hrs_nocturnas_trabajadas
            nominaTemporal.hrs_extras_nocturnas = hrs_extras_nocturnas
            nominaTemporal.hrs_dominical_trabajadas = hrs_dominical_trabajadas
            nominaTemporal.hrs_dominical_nocturnas_trabajadas = hrs_dominical_nocturnas_trabajadas
            nominaTemporal.hrs_semanales_contrato = hrs_semanales_contrato
            nominaTemporal.hrs_extras_normales = hrs_extras_normales
            nominaTemporal.save()
            #Calculamos los nuevos valores a pagar
            pago_hrs_normales_trabajadas = (v_hora_base * nominaTemporal.hrs_normales_trabajadas) * nominaTemporal.dias_trabajados
            pago_hrs_nocturnas_trabajadas = (nominaTemporal.hrs_nocturnas_trabajadas * v_hora_nocturna)
            pago_hrs_extras_nocturnas = (nominaTemporal.hrs_extras_nocturnas * v_hora_ext_nocturna)
            pago_hrs_dominical_trabajadas = (nominaTemporal.hrs_dominical_trabajadas * v_hora_dominical)
            pago_hrs_dominical_nocturnas_trabajadas = (nominaTemporal.hrs_dominical_nocturnas_trabajadas * v_hora_dominical_nocturno)
            pago_hrs_extras_normales = (nominaTemporal.hrs_extras_normales * v_hora_normal_ext)
            #Sumamos los nuevos valores a el salario
            Nuevo_Salario += pago_hrs_normales_trabajadas
            Nuevo_Salario += pago_hrs_nocturnas_trabajadas
            Nuevo_Salario += pago_hrs_extras_nocturnas
            Nuevo_Salario += pago_hrs_dominical_trabajadas
            Nuevo_Salario += pago_hrs_dominical_nocturnas_trabajadas
            Nuevo_Salario += pago_hrs_extras_normales
            nominaTemporal.pago_mes = round(Nuevo_Salario, 2)
            nominaTemporal.save()
            return redirect('nominaEmpleado', empleado_cedula=empleado_cedula,)
    else:
        return render(request, 'error.html', {'error':"Parece que has tratado de acceder a un dato que no es de tu dominio, si crees que es un error contacta a soporte"})
    

#Pago automático de nómina
def pagoNominaMensual(request):
    try:
        idAdministrador = request.user.id
        empleados = Empleado.objects.filter(administrador_id = idAdministrador, en_servicio = True)
        empleados_data = []
        for empleado in empleados:
            empleado_data = {
                "model": "Administracion.empleado",
                "pk": empleado.pk,
                "fields": {
                    "nombres": empleado.nombres,
                    "apellidos": empleado.apellidos,
                    "cargo": empleado.cargo,
                }
            }
            empleados_data.append(empleado_data)
        for pagoEmpleado in empleados_data:
            datosNomina = DatosTemporalesNomina.objects.get(id_empleado = pagoEmpleado['pk'])
            empleado = Empleado.objects.get(id = pagoEmpleado['pk'])
            administrador = request.user
            gestionPago = ConstanciaPago.objects.create(
                nombres = pagoEmpleado['fields']['nombres'],
                apellidos = pagoEmpleado['fields']['apellidos'],
                cargo = pagoEmpleado['fields']['cargo'],
                pago = datosNomina.pago_mes,
                id_empleado = empleado,
                administrador = administrador
            )
            gestionPago.save()

        for empleado in empleados:
            print(empleado.id)
            datosNomina = DatosTemporalesNomina.objects.get(id_empleado = empleado.id)
            print(datosNomina.id)
            # Actualiza la instancia desde la base de datos para restaurar los valores por defecto
            datosNomina.dias_trabajados = DatosTemporalesNomina._meta.get_field('dias_trabajados').default
            datosNomina.hrs_normales_trabajadas = DatosTemporalesNomina._meta.get_field('hrs_normales_trabajadas').default
            datosNomina.hrs_nocturnas_trabajadas = DatosTemporalesNomina._meta.get_field('hrs_nocturnas_trabajadas').default
            datosNomina.hrs_extras_nocturnas = DatosTemporalesNomina._meta.get_field('hrs_extras_nocturnas').default
            datosNomina.hrs_dominical_trabajadas = DatosTemporalesNomina._meta.get_field('hrs_dominical_trabajadas').default
            datosNomina.hrs_dominical_nocturnas_trabajadas = DatosTemporalesNomina._meta.get_field('hrs_dominical_nocturnas_trabajadas').default
            datosNomina.hrs_semanales_contrato = DatosTemporalesNomina._meta.get_field('hrs_semanales_contrato').default
            datosNomina.hrs_extras_normales = DatosTemporalesNomina._meta.get_field('hrs_extras_normales').default
            datosNomina.pago_mes = DatosTemporalesNomina._meta.get_field('pago_mes').default
            print(datosNomina.hrs_nocturnas_trabajadas)
            # Guarda la instancia actualizada
            datosNomina.save()

        return redirect('EMPLEADOS')
    except:
        return render(request, 'error.html', {'error':"Algo salió mal con el pago de la nómina, si el error persiste por favor contacta a soporte"})


