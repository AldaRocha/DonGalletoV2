from django import forms
from medidas_app.models import Medida
from medidas_app import models

class MedidaRegistrarForm(forms.ModelForm):
    class Meta:
        model = Medida
        fields = ["nombre", "nomenclatura"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "nomenclatura": forms.TextInput(attrs={"class": "form-control"})
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class MedidaEditarForm(forms.ModelForm):
    class Meta:
        model = Medida
        fields = ["nombre", "nomenclatura"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "nomenclatura": forms.TextInput(attrs={"class": "form-control"})
        }
    def save(self, id):
        item = models.Medida.objects.filter(id=id).first()
        item.nombre = self.cleaned_data["nombre"]
        item.nomenclatura = self.cleaned_data["nomenclatura"]
        item.save()
        return item