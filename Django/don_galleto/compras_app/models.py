from django.db import models
from django.utils.timezone import now
from proveedores_app.models import Proveedor
from django.contrib.auth.models import User
from insumos_app.models import Insumo

# Create your models here.
class Compra(models.Model):
    fecha_compra = models.DateTimeField(default=now)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=False, blank=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=1)
    def __str__(self):
        return f"{self.id}-{self.fecha_compra}-{self.proveedor}"

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, null=False, blank=False)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, null=False, blank=False)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    precio_unitario = models.DecimalField(max_digits=10 , decimal_places=3)
    fecha_caducidad = models.DateTimeField(default=now)
    def __str__(self):
        return f"{self.id}-{self.compra.id}-{self.insumo.nombre}-{self.cantidad}-{self.precio_unitario}-{self.fecha_caducidad}"