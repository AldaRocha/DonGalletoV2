from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.contrib.auth.models import User
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods

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
    
@require_http_methods(["GET"])
def check_availability(request):
    """
    Vista para verificar si un username o email ya existe en la base de datos
    """
    field = request.GET.get('field')
    value = request.GET.get('value')
    User = get_user_model()
    
    if not field or not value:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)
    
    if field == 'username':
        exists = User.objects.filter(username=value).exists()
    elif field == 'email':
        exists = User.objects.filter(email=value).exists()
    else:
        return JsonResponse({'error': 'Campo no válido'}, status=400)
        
    return JsonResponse({'exists': exists})