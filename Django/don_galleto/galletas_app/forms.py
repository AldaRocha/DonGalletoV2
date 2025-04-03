from django import forms
from galletas_app.models import Galleta
from galletas_app import models

class GalletaRegistrarForm(forms.ModelForm):
    class Meta:
        model = Galleta
        fields = ["nombre", "descripcion", "peso_individual", "imagen"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "peso_individual": forms.NumberInput(attrs={"class": "form-control"}),
            "imagen": forms.FileInput(attrs={"class": "form-control"})
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class GalletaEditarForm(forms.ModelForm):
    class Meta:
        model = Galleta
        fields = ["nombre", "descripcion", "peso_individual", "imagen"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "peso_individual": forms.NumberInput(attrs={"class": "form-control"}),
            "imagen": forms.FileInput(attrs={"class": "form-control"})
        }
    def save(self, id):
        item = models.Galleta.objects.filter(id=id).first()
        item.nombre = self.cleaned_data["nombre"]
        item.descripcion = self.cleaned_data["descripcion"]
        item.peso_individual = self.cleaned_data["peso_individual"]
        if self.cleaned_data.get("imagen"):
            item.imagen = self.cleaned_data["imagen"]
        item.save()
        return item
