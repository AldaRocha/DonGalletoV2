from django import forms
from producciones_app.models import Produccion, SolicitudProduccion
from producciones_app import models
from galletas_app.models import Galleta
from mermas_app.models import Merma
from inventario_galletas_app.models import InventarioGalletas
from django.core.exceptions import ValidationError
from recetas_app.models import Receta, DetalleReceta
from insumos_app.models import Insumo
from compras_app.models import DetalleCompra
from inventario_insumos_app.models import InventarioInsumos
from django.db import transaction
from datetime import datetime, timedelta

class ProduccionRegistrarForm(forms.ModelForm):
    galleta = forms.ModelChoiceField(
        queryset=Galleta.objects.all(),
        label="Galleta",
        empty_label="Seleccione una galleta",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    merma = forms.IntegerField(
        label="Merma",
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    class Meta:
        model = Produccion
        fields = ["cantidad", "galleta"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"class": "form-control"})
        }
    def __init__(self, *args, **kwargs):
        galleta_id = kwargs.pop('galleta_id', None)
        super().__init__(*args, **kwargs)
        if galleta_id and int(galleta_id) > 0:
            self.fields["galleta"].queryset = Galleta.objects.filter(id=galleta_id)
            self.fields["galleta"].initial = Galleta.objects.get(id=galleta_id)
        else:
            self.fields["galleta"].queryset = Galleta.objects.all()
    def save(self, commit=True):
        try:
            with transaction.atomic():
                instance = super().save(commit=False)
                merma = self.cleaned_data["merma"]
                total = self.cleaned_data["cantidad"]
                if merma > total:
                    raise ValidationError("La merma no puede ser mayor que el total")
                galleta = self.cleaned_data["galleta"]
                receta = Receta.objects.filter(galleta_id=galleta.id, para_produccion=True).first()
                if receta is not None:
                    detalle = DetalleReceta.objects.filter(receta_id=receta.id)
                    if detalle.exists():
                        for insumoendetalle in detalle:
                            insumo = Insumo.objects.filter(id=insumoendetalle.insumo_id).first()
                            if insumo is not None:
                                comprasinsumo = DetalleCompra.objects.filter(insumo_id=insumo.id).order_by("fecha_caducidad")
                                if comprasinsumo.exists():
                                    existencia = []
                                    existencia.clear()
                                    for insumocomprado in comprasinsumo:
                                        busqueda = InventarioInsumos.objects.filter(detalle_compra_id=insumocomprado.id, activo=True)
                                        if busqueda.exists():
                                            for obj in busqueda:
                                                existencia.append(obj)
                                    faltapordescontar = insumoendetalle.cantidad + insumoendetalle.merma
                                    insumotomadomerma = InventarioInsumos
                                    for inventario in existencia:
                                        insumotomadomerma = inventario
                                        if faltapordescontar > 0:
                                            if inventario.cantidad_existente >=  faltapordescontar:
                                                inventario.cantidad_existente = inventario.cantidad_existente - faltapordescontar
                                                if inventario.cantidad_existente <= 0:
                                                    inventario.activo = False
                                                inventario.save()
                                                faltapordescontar = 0
                                            else:
                                                faltapordescontar = insumoendetalle.cantidad - inventario.cantidad_existente
                                                inventario.cantidad_existente = 0
                                                inventario.activo = False
                                                inventario.save()
                                        else:
                                            break
                                    if faltapordescontar > 0:
                                        raise ValidationError(f"No tienes el insumo suficiente para producir: {insumoendetalle.insumo}")
                                    Merma.objects.create(
                                        tipo_merma="Produccion",
                                        cantidad=insumoendetalle.merma,
                                        insumo=insumotomadomerma
                                    )
                                    solicitud = SolicitudProduccion.objects.filter(galleta_id=galleta.id)
                                    if solicitud is not None:
                                        solicitud.delete()
                                else:
                                    raise ValidationError(f"No se compro el insumo: {insumoendetalle.insumo}")
                            else:
                                raise ValidationError(f"No se encontraron el insumo: {insumoendetalle.insumo}")
                    else:
                        raise ValidationError("No se encontraron los ingredientes para esta receta")
                else:
                    raise ValidationError("No hay una receta activa para producir la galleta")
                if commit:
                    instance.save()
                    self.save_m2m()
                    if merma > 0:
                        Merma.objects.create(
                            tipo_merma="Produccion",
                            cantidad=merma,
                            produccion=instance
                        )
                    InventarioGalletas.objects.create(
                        precio_por_galleta=galleta.precio_venta,
                        cantidad=total-merma,
                        fecha_caducidad=datetime.now() + timedelta(days=3),
                        produccion=instance
                    )
                return instance
        except Exception as ex:
            raise ValidationError(f"Error: {ex}")

class ProduccionEditarForm(forms.ModelForm):
    merma = forms.IntegerField(
        label="Merma",
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    class Meta:
        model = Produccion
        fields = ["cantidad"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"class": "form-control"})
        }
    def save(self, id):
        merma = self.cleaned_data["merma"]
        total = self.cleaned_data["cantidad"]
        if merma > total:
            raise ValidationError("La merma no puede ser mayor que el total")
        item = models.Produccion.objects.filter(id=id).first()
        item.cantidad = self.cleaned_data["cantidad"]
        item.save()
        filamerma = Merma.objects.filter(produccion_id=item.id).first()
        filamerma.cantidad = merma
        filamerma.save()
        return item
