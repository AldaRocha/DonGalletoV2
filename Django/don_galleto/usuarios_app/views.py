from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.contrib.auth.models import User
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
class ListaUsuariosView(PermissionRequiredMixin, TemplateView):
    permission_required = ["usuarios_app.view_User"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "lista_usuarios.html"
    def get_context_data(self):
        lista = User.objects.all()
        return {
            "lista": lista
        }

class CrearUsuariosView(PermissionRequiredMixin, FormView):
    permission_required = ["usuarios_app.add_User"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "crear_usuarios.html"
    form_class = forms.UsuarioRegistroForm
    success_url = reverse_lazy("lista_usuarios")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class EditarUsuariosView(PermissionRequiredMixin, FormView):
    permission_required = ["usuarios_app.edit_User"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "editar_usuarios.html"
    form_class = forms.UsuarioEditarForm
    success_url = reverse_lazy("lista_usuarios")
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        usuario = get_object_or_404(User, id=id)
        kwargs["instance"] = usuario
        return kwargs
    def form_valid(self, form):
        form.save(self.kwargs.get("id"))
        return super().form_valid(form)