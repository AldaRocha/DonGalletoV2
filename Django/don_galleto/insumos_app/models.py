from django.db import models
from medidas_app.models import Medida

# Create your models here.
class Insumo(models.Model):
    nombre = models.TextField(max_length=100)
    descripcion = models.TextField(max_length=500)
    medida = models.ForeignKey(Medida, on_delete=models.CASCADE, null=False, blank=False)
    cantidad_minima = models.IntegerField(null=False, default=0)
    def __str__(self):
        return f"{self.nombre} / {self.medida.nombre}"