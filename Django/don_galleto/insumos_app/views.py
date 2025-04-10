from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from insumos_app.models import Insumo
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
class ListaInsumosView(PermissionRequiredMixin, TemplateView):
    permission_required = ["insumos_app.view_Insumo"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "lista_insumos.html"
    def get_context_data(self):
        lista = Insumo.objects.all()
        return {
            "lista": lista
        }

class CrearInsumosView(PermissionRequiredMixin, FormView):
    permission_required = ["insumos_app.add_Insumo"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "crear_insumos.html"
    form_class = forms.InsumoRegistrarForm
    success_url = reverse_lazy("lista_insumos")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class EditarInsumosView(PermissionRequiredMixin, FormView):
    permission_required = ["insumos_app.edit_Insumo"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "editar_insumos.html"
    form_class = forms.InsumoEditarForm
    success_url = reverse_lazy("lista_insumos")
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        insumo = get_object_or_404(Insumo, id=id)
        kwargs["instance"] = insumo
        return kwargs
    def form_valid(self, form):
        form.save(self.kwargs.get("id"))
        return super().form_valid(form)

def EliminarInsumoView(request, pk):
    if request.method == "POST":
        insumo = get_object_or_404(Insumo, pk=pk)
        insumo.delete()
        return redirect(reverse_lazy("lista_insumos"))
    else:
        return redirect(reverse_lazy("lista_insumos"))