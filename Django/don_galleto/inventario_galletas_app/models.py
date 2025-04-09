from django.db import models
from django.utils.timezone import now
from producciones_app.models import Produccion

# Create your models here.
class InventarioGalletas(models.Model):
    precio_por_galleta = models.DecimalField(decimal_places=3, max_digits=10)
    cantidad = models.IntegerField(null=False)
    fecha_caducidad = models.DateTimeField(default=now)
    produccion = models.ForeignKey(Produccion, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return f"{self.id}-{self.precio_por_galleta}-{self.fecha_caducidad}-{self.produccion}"