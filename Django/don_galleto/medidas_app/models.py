from django.db import models

# Create your models here.
class Medida(models.Model):
    nombre = models.TextField(max_length=50, null=False)
    nomenclatura = models.TextField(max_length=5, null=False)
    def _str_(self):
        return f"{self.id}-{self.tipoMedida}"