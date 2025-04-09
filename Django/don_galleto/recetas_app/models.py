from django.db import models
from galletas_app.models import Galleta
from insumos_app.models import Insumo

# Create your models here.
class Receta(models.Model):
    nombre = models.TextField(max_length=100)
    descripcion = models.TextField(max_length=1000)
    para_produccion = models.BooleanField(default=False)
    galleta = models.ForeignKey(Galleta, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return f"{self.id}-{self.nombre}-{self.descripcion}-{self.galleta.nombre}-{self.para_produccion}"

class DetalleReceta(models.Model):
    cantidad = models.DecimalField(decimal_places=3, max_digits=10)
    merma = models.DecimalField(decimal_places=3, max_digits=10)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, null=False, blank=False)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return f"{self.id}-{self.cantidad}-{self.merma}-{self.receta.nombre}-{self.insumo.nombre}"
