from django.db import models

# Modelo: Receta
class Receta(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre de la receta
    descripcion = models.TextField(blank=True, null=True)  # Descripción de la receta
    ingredientes = models.ManyToManyField('almacen_app.Insumo', through='DetalleReceta')  # Relación con insumos

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'


class DetalleReceta(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)  # Relación con la receta
    insumo = models.ForeignKey('almacen_app.Insumo', on_delete=models.CASCADE)  # Relación con el insumo
    cantidad = models.DecimalField(max_digits=18, decimal_places=2)  # Cantidad de insumo en la receta

    def __str__(self):
        return f"{self.receta.nombre} - {self.insumo.nombre}"

    class Meta:
        verbose_name = 'Detalle Receta'
        verbose_name_plural = 'Detalles Receta'
