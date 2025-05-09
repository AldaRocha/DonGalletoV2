# Generated by Django 5.1.7 on 2025-04-09 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galletas_app', '0002_galleta_medida'),
        ('ventas_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('galleta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='galletas_app.galleta')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas_app.venta')),
            ],
        ),
    ]
