from django.db import models

# Create your models here.
class Medida(models.Model):
    nombre = models.TextField(max_length=50, null=False)
    nomenclatura = models.TextField(max_length=5, null=False)
    def __str__(self):
        return f"{self.nombre}"