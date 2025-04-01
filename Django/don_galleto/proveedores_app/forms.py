from django import forms
from proveedores_app.models import Proveedor
from proveedores_app import models

class ProveedorRegistrarForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombre", "email", "telefono", "direccion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"})
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class ProveedorEditarForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombre", "email", "telefono", "direccion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"})
        }
    def save(self, id):
        item = models.Proveedor.objects.filter(id=id).first()
        item.nombre = self.cleaned_data["nombre"]
        item.email = self.cleaned_data["email"]
        item.telefono = self.cleaned_data["telefono"]
        item.direccion = self.cleaned_data["direccion"]
        item.save()
        return item