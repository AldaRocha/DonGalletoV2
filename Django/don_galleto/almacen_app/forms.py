from django import forms
from .models import Proveedor, Insumo, Compra, Merma

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono', 'direccion']

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'descripcion', 'unidad_medida']

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['fecha_compra', 'proveedor', 'total']

class MermaForm(forms.ModelForm):
    class Meta:
        model = Merma
        fields = ['tipo', 'cantidad', 'insumo', 'galleta']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['insumo'].queryset = Insumo.objects.all()