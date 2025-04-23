from django import forms
from galletas_app.models import Galleta
from galletas_app import models
from medidas_app.models import Medida
from producciones_app.models import SolicitudProduccion
from decimal import Decimal, ROUND_HALF_UP

class GalletaRegistrarForm(forms.ModelForm):
    medida = forms.ModelChoiceField(
        queryset=Medida.objects.all(),
        label="Medida",
        empty_label="Seleccione una medida",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = Galleta
        fields = ["nombre", "descripcion", "peso_individual", "precio_produccion", "precio_venta", "imagen", "medida"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "peso_individual": forms.NumberInput(attrs={"class": "form-control"}),
            "precio_produccion": forms.NumberInput(attrs={"class": "form-control"}),
            "precio_venta": forms.NumberInput(attrs={"class": "form-control"}),
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
        fields = ['nombre', 'descripcion', 'peso_individual', 'precio_produccion', 'precio_venta', 'medida', 'imagen']
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "peso_individual": forms.NumberInput(attrs={"class": "form-control"}),
            "precio_venta": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "imagen": forms.FileInput(attrs={"class": "form-control"})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            precio = instance.precio_produccion_actual
            precio_redondeado = Decimal(str(precio)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            self.initial['precio_produccion'] = precio_redondeado

        self.fields['precio_produccion'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'step': '0.01',
            'min': '0',
            'max': '99999.99'
        })

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.cleaned_data.get('imagen') is None:
            # Mantener la imagen existente si no se proporciona una nueva
            instance.imagen = instance.imagen
            
        if commit:
            instance.save()
            
        return instance