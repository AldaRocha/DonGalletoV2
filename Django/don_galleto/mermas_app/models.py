from django.db import models
from django.utils.timezone import now
from inventario_insumos_app.models import InventarioInsumos
from producciones_app.models import Produccion

# Create your models here.
class Merma(models.Model):
    tipo_merma = models.TextField(max_length=100)
    cantidad = models.DecimalField(decimal_places=3, max_digits=10)
    fecha_registro = models.DateTimeField(default=now)
    insumo = models.ForeignKey(InventarioInsumos, on_delete=models.CASCADE, null=True, blank=True)
    produccion = models.ForeignKey(Produccion, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.id}-{self.tipo_merma}-{self.cantidad}-{self.fecha_registro}-{self.insumo}-{self.produccion}"