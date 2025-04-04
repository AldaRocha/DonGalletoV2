from django import forms
from insumos_app.models import Insumo
from insumos_app import models
from medidas_app.models import Medida

class InsumoRegistrarForm(forms.ModelForm):
    medida = forms.ModelChoiceField(
        queryset=Medida.objects.all(),
        label="Medida",
        empty_label="Seleccione una medida",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = Insumo
        fields = ["nombre", "descripcion", "medida", "cantidad_minima"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad_minima": forms.NumberInput(attrs={"class": "form-control"})
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class InsumoEditarForm(forms.ModelForm):
    medida = forms.ModelChoiceField(
        queryset=Medida.objects.all(),
        label="Medida",
        empty_label="Seleccione una medida",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = Insumo
        fields = ["nombre", "descripcion", "medida", "cantidad_minima"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad_minima": forms.NumberInput(attrs={"class": "form-control"})
        }
    def save(self, id):
        item = models.Insumo.objects.filter(id=id).first()
        item.nombre = self.cleaned_data["nombre"]
        item.descripcion = self.cleaned_data["descripcion"]
        item.medida = self.cleaned_data["medida"]
        item.cantidad_minima = self.cleaned_data["cantidad_minima"]
        item.save()
        return item