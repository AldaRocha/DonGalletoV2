from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.TextInput(attrs={"class": "form-control"}),
            "password2": forms.TextInput(attrs={"class": "form-control"})
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
            grupo = Group.objects.filter(id=2).first()
            grupo.user_set.add(user)
        return user