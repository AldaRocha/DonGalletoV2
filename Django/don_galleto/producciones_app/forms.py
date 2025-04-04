from django import forms
from producciones_app.models import Produccion
from producciones_app import models
from galletas_app.models import Galleta
from django.core.exceptions import ValidationError

class ProduccionRegistrarForm(forms.ModelForm):
    galleta = forms.ModelChoiceField(
        queryset=Galleta.objects.all(),
        label="Galleta",
        empty_label="Seleccione una galleta",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = Produccion
        fields = ["cantidad", "galleta"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"class": "form-control"})
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class ProduccionEditarForm(forms.ModelForm):
    galleta = forms.ModelChoiceField(
        queryset=Galleta.objects.all(),
        label="Galleta",
        empty_label="Seleccione una galleta",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = Produccion
        fields = ["cantidad", "galleta"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"class": "form-control"})
        }
    def save(self, id):
        item = models.Produccion.objects.filter(id=id).first()
        item.cantidad = self.cleaned_data["cantidad"]
        item.galleta = self.cleaned_data["galleta"]
        item.save()
        return item
