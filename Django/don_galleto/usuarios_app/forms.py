from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

class UsuarioRegistroForm(UserCreationForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        label="Grupo"
    )
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2", "is_active", "grupo"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.TextInput(attrs={"class": "form-control"}),
            "password2": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado")
        return email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            grupo = self.cleaned_data["grupo"]
            grupo.user_set.add(user)
        return user

class UsuarioEditarForm(UserCreationForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        label="Grupo"
    )
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2", "is_active", "grupo"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.TextInput(attrs={"class": "form-control"}),
            "password2": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.groups.exists():
            self.fields['grupo'].initial = self.instance.groups.first()
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password1"].required = False
        self.fields["password2"].required = False
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este correo electrónico ya está registrado")
        return email
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Ya existe un usuario con este nombre.")
        return username
    def save(self, id):
        item = User.objects.filter(id=id).first()
        item.first_name = self.cleaned_data["first_name"]
        item.last_name = self.cleaned_data["last_name"]
        item.email = self.cleaned_data["email"]
        item.username = self.cleaned_data["username"]
        if self.cleaned_data.get("password1") and self.cleaned_data.get("password2"):
            if self.cleaned_data["password1"] == self.cleaned_data["password2"]:
                item.set_password(self.cleaned_data["password2"])
        item.is_active = self.cleaned_data["is_active"]
        item.save()
        grupo = self.cleaned_data["grupo"]
        item.groups.set([grupo])
        return item