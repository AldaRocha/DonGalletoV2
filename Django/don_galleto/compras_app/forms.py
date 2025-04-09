from django import forms
from compras_app.models import Compra, DetalleCompra
from compras_app import models
from proveedores_app.models import Proveedor
from django.contrib.auth.models import User
from insumos_app.models import Insumo
from inventario_insumos_app.models import InventarioInsumos

class CompraRegistrarForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        label="Proveedor",
        empty_label="Seleccione un proveedor",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    usuario = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="Administrador"),
        label="Realizado por",
        empty_label="Selecciona el usuario",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = Compra
        fields = ["proveedor", "usuario"]
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class CompraEditarForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        label="Proveedor",
        empty_label="Seleccione un proveedor",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    usuario = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="Administrador"),
        label="Realizado por",
        empty_label="Selecciona el usuario",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = Compra
        fields = ["proveedor", "usuario"]
    def save(self, id):
        item = models.Compra.objects.filter(id=id).first()
        item.proveedor = self.cleaned_data["proveedor"]
        item.usuario = self.cleaned_data["usuario"]
        item.save()
        return item

class DetalleCompraRegistrarForm(forms.ModelForm):
    insumo = forms.ModelChoiceField(
        queryset=Insumo.objects.all(),
        label="Insumo",
        empty_label="Seleccione un insumo",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = DetalleCompra
        fields = ["insumo", "cantidad", "precio_unitario", "fecha_caducidad"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"class": "form-control"}),
            "precio_unitario": forms.NumberInput(attrs={"class": "form-control"}),
            "fecha_caducidad": forms.DateInput(attrs={"class": "form-control", "type": "date"})
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
            InventarioInsumos.objects.create(
                detalle_compra=instance,
                cantidad_existente=instance.cantidad
            )
        return instance

class DetalleCompraEditarForm(forms.ModelForm):
    insumo = forms.ModelChoiceField(
        queryset=Insumo.objects.all(),
        label="Insumo",
        empty_label="Seleccione un insumo",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = DetalleCompra
        fields = ["insumo", "cantidad", "precio_unitario", "fecha_caducidad"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"class": "form-control"}),
            "precio_unitario": forms.NumberInput(attrs={"class": "form-control"}),
            "fecha_caducidad": forms.DateInput(attrs={"class": "form-control", "type": "date"}, format='%Y-%m-%d')
        }
    def save(self, id):
        item = models.DetalleCompra.objects.filter(id=id).first()
        item.insumo = self.cleaned_data["insumo"]
        item.cantidad = self.cleaned_data["cantidad"]
        item.precio_unitario = self.cleaned_data["precio_unitario"]
        item.fecha_caducidad = self.cleaned_data["fecha_caducidad"]
        item.save()
        inventario = InventarioInsumos.objects.filter(detalle_compra_id=id).first()
        inventario.cantidad_existente = self.cleaned_data["cantidad"]
        inventario.save()
        return item