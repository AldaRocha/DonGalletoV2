from django import forms
from recetas_app.models import Receta, DetalleReceta
from recetas_app import models
from galletas_app.models import Galleta
from insumos_app.models import Insumo

class RecetaRegistrarForm(forms.ModelForm):
    galleta = forms.ModelChoiceField(
        queryset=Galleta.objects.all(),
        label="Galleta",
        empty_label="Seleccione una galleta",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = Receta
        fields = ["nombre", "descripcion", "para_produccion", "galleta"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "para_produccion": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class RecetaEditarForm(forms.ModelForm):
    galleta = forms.ModelChoiceField(
        queryset=Galleta.objects.all(),
        label="Galleta",
        empty_label="Seleccione una galleta",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = Receta
        fields = ["nombre", "descripcion", "para_produccion", "galleta"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "para_produccion": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }
    def save(self, id):
        item = models.Receta.objects.filter(id=id).first()
        item.nombre = self.cleaned_data["nombre"]
        item.descripcion = self.cleaned_data["descripcion"]
        item.para_produccion = self.cleaned_data["para_produccion"]
        item.galleta = self.cleaned_data["galleta"]
        item.save()
        return item

class DetalleRecetaRegistrarForm(forms.ModelForm):
    insumo = forms.ModelChoiceField(
        queryset=Insumo.objects.all(),
        label="Insumo",
        empty_label="Seleccione un insumo",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = DetalleReceta
        fields = ["cantidad", "merma", "insumo"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"class": "form-control"}),
            "merma": forms.NumberInput(attrs={"class": "form-control"})
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class DetalleRecetaEditarForm(forms.ModelForm):
    insumo = forms.ModelChoiceField(
        queryset=Insumo.objects.all(),
        label="Insumo",
        empty_label="Seleccione un insumo",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = DetalleReceta
        fields = ["cantidad", "merma", "insumo"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"class": "form-control"}),
            "merma": forms.NumberInput(attrs={"class": "form-control"})
        }
    def save(self, id):
        item = models.DetalleReceta.objects.filter(id=id).first()
        item.cantidad = self.cleaned_data["cantidad"]
        item.merma = self.cleaned_data["merma"]
        item.insumo = self.cleaned_data["insumo"]
        item.save()
        return item
