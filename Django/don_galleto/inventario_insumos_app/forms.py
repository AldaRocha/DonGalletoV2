from django import forms
from inventario_insumos_app.models import InventarioInsumos
from inventario_insumos_app import models
from compras_app.models import DetalleCompra

class InventarioInsumosRegistrarForm(forms.ModelForm):
    detalle_compra = forms.ModelChoiceField(
        queryset=DetalleCompra.objects.all(),
        label="Detalle de compra",
        empty_label="Seleccione un detalle",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = InventarioInsumos
        fields = ["detalle_compra", "cantidad_existente"]
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class InventarioInsumosEditarForm(forms.ModelForm):
    detalle_compra = forms.ModelChoiceField(
        queryset=DetalleCompra.objects.all(),
        label="Detalle de compra",
        empty_label="Seleccione un detalle",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = InventarioInsumos
        fields = ["detalle_compra", "cantidad_existente"]
    def save(self, id):
        item = models.InventarioInsumos.objects.filter(id=id).first()
        item.detalle_compra = self.cleaned_data["detalle_compra"]
        item.cantidad_existente = self.cleaned_data["cantidad_existente"]
        item.save()
        return item