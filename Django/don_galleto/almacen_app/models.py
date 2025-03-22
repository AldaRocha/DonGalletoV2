from django.db import models
from recetas_app.models import Receta  # Importación de Receta

# Modelo: Galleta
class Galleta(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre de la galleta
    descripcion = models.TextField(blank=True, null=True)  # Descripción de la galleta
    precio_venta = models.DecimalField(max_digits=18, decimal_places=2)  # Precio de venta
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)  # Relación con la receta

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Galleta'
        verbose_name_plural = 'Galletas'



class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'


class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'


class Compra(models.Model):
    fecha_compra = models.DateTimeField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return f"Compra {self.id} - {self.fecha_compra}"

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, related_name="detalles", on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=18, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=2)
    total = models.DecimalField(max_digits=18, decimal_places=2)
    fecha_caducidad = models.DateTimeField()

    def __str__(self):
        return f"Detalle Compra {self.id}"

    class Meta:
        verbose_name = 'Detalle Compra'
        verbose_name_plural = 'Detalles Compra'


class InventarioInsumo(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=18, decimal_places=2)
    cantidad_minima = models.DecimalField(max_digits=18, decimal_places=2)
    fecha_caducidad = models.DateTimeField()

    def __str__(self):
        return f"{self.insumo.nombre} - {self.cantidad} disponibles"


class InventarioGalleta(models.Model):
    galleta = models.ForeignKey(Galleta, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_caducidad = models.DateTimeField()

    def __str__(self):
        return f"{self.galleta.nombre} - {self.cantidad} disponibles"


class Merma(models.Model):
    tipo = models.CharField(max_length=20)
    cantidad = models.DecimalField(max_digits=18, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    insumo = models.ForeignKey(Insumo, null=True, blank=True, on_delete=models.CASCADE)
    galleta = models.ForeignKey(Galleta, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        
        return f"Merma de {self.tipo} - {self.cantidad} unidades"
