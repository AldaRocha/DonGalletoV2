# Generated by Django 5.1.7 on 2025-04-09 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario_insumos_app', '0002_inventarioinsumos_activo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventarioinsumos',
            name='cantidad_existente',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]
