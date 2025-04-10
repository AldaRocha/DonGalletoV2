from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from galletas_app.models import Galleta

# Create your models here.
class Venta(models.Model):
    fecha_venta = models.DateTimeField(default=now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return f"{self.id}-{self.fecha_venta}-{self.usuario}"

class DetalleVenta(models.Model):
    cantidad = models.IntegerField(null=False)
    precio = models.DecimalField(decimal_places=2, max_digits=10)
    subtotal = models.DecimalField(decimal_places=2, max_digits=10)
    galleta = models.ForeignKey(Galleta, on_delete=models.CASCADE, null=False, blank=False)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return f"{self.cantidad}-{self.precio}-{self.subtotal}-{self.galleta}-{self.venta}"