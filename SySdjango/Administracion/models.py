from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Empleado(models.Model):
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    salario = models.FloatField()
    cedula = models.IntegerField(unique=True)
    en_servicio = models.BooleanField(default=True)

    administrador = models.ForeignKey(User, on_delete=models.CASCADE)
    def _str_(self):
        return f"Empleado {self.id}: {self.nombres} {self.apellidos} - {self.cargo}"
    
class HistorialEmpleado(models.Model):
    #Datos anteriores
    ant_nombres = models.CharField(max_length=30)
    ant_apellidos = models.CharField(max_length=30)
    ant_cargo = models.CharField(max_length=100)
    ant_telefono = models.CharField(max_length=20)
    ant_direccion = models.CharField(max_length=200)
    ant_salario = models.FloatField()
    ant_en_servicio = models.BooleanField()
    #Datos actualizados
    act_nombres = models.CharField(max_length=30)
    act_apellidos = models.CharField(max_length=30)
    act_cargo = models.CharField(max_length=100)
    act_telefono = models.CharField(max_length=20)
    act_direccion = models.CharField(max_length=200)
    act_salario = models.FloatField()
    act_en_servicio = models.BooleanField()
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    administrador = models.ForeignKey(User, on_delete=models.CASCADE)
    def _str_(self):
        return f"Empleado {self.id}: {self.act_nombres} {self.act_apellidos} - {self.act_cargo}"

class DatosTemporalesNomina(models.Model):
    dias_trabajados = models.IntegerField(default=30)
    hrs_normales_trabajadas = models.IntegerField(default=8)
    hrs_nocturnas_trabajadas = models.IntegerField(default=0)
    hrs_extras_nocturnas = models.IntegerField(default=0)
    hrs_dominical_trabajadas = models.IntegerField(default=0)
    hrs_dominical_nocturnas_trabajadas = models.IntegerField(default=0)
    hrs_semanales_contrato = models.IntegerField(default=40)
    hrs_extras_normales = models.IntegerField(default=0)
    pago_mes = models.FloatField(default=0)

    id_empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
    administrador = models.ForeignKey(User, on_delete=models.CASCADE)
    def _str_(self):
        return f"Empleado {self.id}: {self.act_nombres} {self.act_apellidos} - valor a pagar {self.pago_mes}"

class ConstanciaPago(models.Model):
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    cargo = models.CharField(max_length=100)
    pago = models.FloatField()
    fecha_pago = models.DateTimeField(auto_now_add=True)

    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    administrador = models.ForeignKey(User, on_delete=models.CASCADE)
    def _str_(self):
        return f"Empleado {self.id}: {self.nombres} {self.apellidos} - valor pagado: {self.pago} en la fecha {self.fecha_pago}"

