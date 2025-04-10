from django.db import models
from compras_app.models import DetalleCompra

# Create your models here.
class InventarioInsumos(models.Model):
    detalle_compra = models.ForeignKey(DetalleCompra, on_delete=models.CASCADE, null=False, blank=False)
    cantidad_existente = models.DecimalField(decimal_places=3, max_digits=10)
    activo = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.detalle_compra.insumo}"