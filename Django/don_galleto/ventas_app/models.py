from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Venta(models.Model):
    fecha_venta = models.DateTimeField(default=now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return f"{self.id}-{self.fecha_venta}-{self.usuario}"