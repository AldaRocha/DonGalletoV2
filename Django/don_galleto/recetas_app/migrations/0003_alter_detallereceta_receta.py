# Generated by Django 5.1.7 on 2025-04-11 22:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recetas_app', '0002_alter_detallereceta_merma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallereceta',
            name='receta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='recetas_app.receta'),
        ),
    ]
