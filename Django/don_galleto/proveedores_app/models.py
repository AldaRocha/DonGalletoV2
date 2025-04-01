from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre = models.TextField(max_length=100)
    email = models.TextField(max_length=100)
    telefono = models.TextField(max_length=15)
    direccion = models.TextField(max_length=200)
    def __str__(self):
        return f"{self.nombre} / {self.email}"