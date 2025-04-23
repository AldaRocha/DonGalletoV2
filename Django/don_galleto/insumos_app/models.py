from django.db import models
from medidas_app.models import Medida

# Create your models here.
class Insumo(models.Model):
    nombre = models.TextField(max_length=100)
    descripcion = models.TextField(max_length=500)
    medida = models.ForeignKey(Medida, on_delete=models.CASCADE, null=False, blank=False)
    cantidad_minima = models.DecimalField(decimal_places=3, max_digits=10, null=False, default=0)
    precio = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=0)

    def __str__(self):
        return f"{self.nombre} / {self.medida.nombre}"