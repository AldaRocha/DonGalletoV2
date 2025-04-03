from django.db import models
from compras_app.models import DetalleCompra

# Create your models here.
class InventarioInsumos(models.Model):
    detalle_compra = models.ForeignKey(DetalleCompra, on_delete=models.CASCADE, null=False, blank=False)
    cantidad_existente = models.IntegerField(null=False)
    def __str__(self):
        return f"{self.id}-{self.detalle_compra.insumo.nombre}-{self.cantidad_existente}-{self.cantidad_minima}"