from django import forms
from galletas_app.models import Galleta
from galletas_app import models
from medidas_app.models import Medida
from producciones_app.models import SolicitudProduccion

class GalletaRegistrarForm(forms.ModelForm):
    medida = forms.ModelChoiceField(
        queryset=Medida.objects.all(),
        label="Medida",
        empty_label="Seleccione una medida",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = Galleta
        fields = ["nombre", "descripcion", "peso_individual", "imagen", "medida"]
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

            SolicitudProduccion.objects.create(
                galleta=instance
            )

            self.save_m2m()
        return instance

class GalletaEditarForm(forms.ModelForm):
    medida = forms.ModelChoiceField(
        queryset=Medida.objects.all(),
        label="Medida",
        empty_label="Seleccione una medida",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = Galleta
        fields = ["nombre", "descripcion", "peso_individual", "imagen", "medida"]
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
        item.medida = self.cleaned_data["medida"]
        item.save()
        return item
