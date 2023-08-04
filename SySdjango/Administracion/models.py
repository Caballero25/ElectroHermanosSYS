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

    administrador = models.ForeignKey(User, on_delete=models.CASCADE)
    def _str_(self):
        return f"Empleado {self.id}: {self.nombres} {self.apellidos} - {self.cargo}"


class Inventario(models.Model):
    nombre_producto = models.CharField(max_length=100)
    marca_producto = models.CharField(max_length=100)
    precio_unidad = models.FloatField()
    cantidad_disponible = models.IntegerField()

    administrador = models.ForeignKey(User, on_delete=models.CASCADE)
    def _str_(self):
        return f"Producto {self.id}: {self.nombre_producto} {self.marca_producto} - {self.precio_unidad}"


class Proveedores(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    producto_distribuido = models.CharField(max_length=100)
    precio_unidad = models.FloatField()

    administrador = models.ForeignKey(User, on_delete=models.CASCADE)
    def _str_(self):
        return f"Producto {self.producto_distribuido}: distribuido por {self.nombre_empresa} costo - {self.precio_unidad}/Unidad"
    
class HistorialVentas(models.Model):
    fecha_venta = models.DateTimeField(auto_now_add=True)
    producto_vendido = models.CharField(max_length=100)
    marca_producto = models.CharField(max_length=100)
    precio_unidad = models.FloatField()
    unidades_vendidas = models.IntegerField()
    total_venta = models.FloatField()

    administrador = models.ForeignKey(User, on_delete=models.CASCADE)
    def _str_(self):
        return f"Venta #{self.id}: fecha: {self.fecha_venta} | {self.producto_vendido} - {self.marca_producto} - {self.precio_unidad} - {self.unidades_vendidas}. Total: ${self.total_venta}"


class HistorialCompras(models.Model):
    fecha_compra = models.DateTimeField(auto_now_add=True)
    producto_comprado = models.CharField(max_length=100)
    marca_producto = models.CharField(max_length=100)
    precio_unidad = models.FloatField()
    unidades_compradas = models.IntegerField()
    total_compra = models.FloatField()

    administrador = models.ForeignKey(User, on_delete=models.CASCADE)
    def _str_(self):
        return f"Compra #{self.id}: fecha: {self.fecha_compra} | {self.producto_comprado} - {self.marca_producto} - {self.precio_unidad} - {self.unidades_compradas}. Total: ${self.total_compra}"