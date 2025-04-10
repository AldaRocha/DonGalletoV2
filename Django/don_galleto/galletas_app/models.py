from django.db import models
from medidas_app.models import Medida

# Create your models here.
class Galleta(models.Model):
    nombre = models.TextField(max_length=100)
    descripcion = models.TextField(max_length=1000)
    peso_individual = models.DecimalField(decimal_places=3, max_digits=10)
    precio_produccion = models.DecimalField(decimal_places=2, max_digits=10)
    precio_venta = models.DecimalField(decimal_places=2, max_digits=10)
    imagen = models.ImageField(upload_to="Galletas/", null=False, blank=False)
    medida = models.ForeignKey(Medida, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"