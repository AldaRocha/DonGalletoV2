from django.db import models
from insumos_app.models import Insumo
from decimal import Decimal
from compras_app.models import DetalleCompra 

# Create your models here.
class Receta(models.Model):
    nombre = models.TextField(max_length=100)
    descripcion = models.TextField(max_length=1000)
    para_produccion = models.BooleanField(default=False)
    galleta = models.ForeignKey('galletas_app.Galleta', on_delete=models.CASCADE, null=False, blank=False)

    @property
    def costo_total_insumos(self):
        # Sum the total cost of all related DetalleReceta instances
        return sum(detalle.costo_total for detalle in self.detalles.all())

    @property
    def costo_por_galleta(self):
        # Divide the total cost by 30 (number of cookies per batch)
        costo_total = self.costo_total_insumos
        return costo_total / Decimal('30') if costo_total > 0 else Decimal('0')


class DetalleReceta(models.Model):
    receta = models.ForeignKey(
        'Receta',
        on_delete=models.CASCADE,
        related_name='detalles'  # Ensure this is set
    )
    insumo = models.ForeignKey('insumos_app.Insumo', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    merma = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    @property
    def costo_total(self):
        # Calculate the total cost for this detail
        cantidad_total = self.cantidad + self.merma
        ultimo_precio = DetalleCompra.objects.filter(insumo=self.insumo).order_by('-compra__fecha_compra').first()
        precio_unitario = ultimo_precio.precio_unitario if ultimo_precio else Decimal('0')
        return cantidad_total * precio_unitario
