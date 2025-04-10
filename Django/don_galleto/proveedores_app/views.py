from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from proveedores_app.models import Proveedor
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
class ListaProveedoresView(PermissionRequiredMixin, TemplateView):
    permission_required = ["proveedores_app.view_Proveedor"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "lista_proveedores.html"
    def get_context_data(self):
        lista = Proveedor.objects.all()
        return {
            "lista": lista
        }

class CrearProveedoresView(PermissionRequiredMixin, FormView):
    permission_required = ["proveedores_app.add_Proveedor"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "crear_proveedores.html"
    form_class = forms.ProveedorRegistrarForm
    success_url = reverse_lazy("lista_proveedores")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class EditarProveedoresView(PermissionRequiredMixin, FormView):
    permission_required = ["proveedores_app.edit_Proveedor"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "editar_proveedores.html"
    form_class = forms.ProveedorEditarForm
    success_url = reverse_lazy("lista_proveedores")
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        proveedor = get_object_or_404(Proveedor, id=id)
        kwargs["instance"] = proveedor
        return kwargs
    def form_valid(self, form):
        form.save(self.kwargs.get("id"))
        return super().form_valid(form)