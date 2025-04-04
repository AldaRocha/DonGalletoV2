from django.db import models
from django.utils.timezone import now
from galletas_app.models import Galleta

# Create your models here.
class Produccion(models.Model):
    cantidad = models.IntegerField(null=False)
    fecha_preparacion = models.DateTimeField(default=now)
    galleta = models.ForeignKey(Galleta, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return f"{self.id}-{self.cantidad}-{self.fecha_preparacion}-{self.galleta}"