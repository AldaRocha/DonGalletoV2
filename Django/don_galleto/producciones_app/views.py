from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from producciones_app.models import Produccion, SolicitudProduccion
from . import forms
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from mermas_app.models import Merma
from recetas_app.models import Receta
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
class ListaProduccionesView(PermissionRequiredMixin, TemplateView):
    permission_required = ["producciones_app.view_Produccion"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "lista_producciones.html"
    def get_context_data(self):
        lista = Produccion.objects.all()
        return {
            "lista": lista
        }

class CrearProduccionesView(PermissionRequiredMixin, FormView):
    permission_required = ["producciones_app.add_Produccion"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "crear_producciones.html"
    form_class = forms.ProduccionRegistrarForm
    success_url = reverse_lazy("lista_producciones")
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        kwargs["galleta_id"] = id
        return kwargs
    def form_valid(self, form):
        try:
            form.save()
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

class EditarProduccionesView(PermissionRequiredMixin, FormView):
    permission_required = ["producciones_app.edit_Produccion"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "editar_producciones.html"
    form_class = forms.ProduccionEditarForm
    success_url = reverse_lazy("lista_producciones")
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        produccion = get_object_or_404(Produccion, id=id)
        kwargs["instance"] = produccion
        merma = Merma.objects.filter(produccion_id=produccion.id).first()
        if merma:
            kwargs["initial"] = {"merma": merma.cantidad}
        return kwargs
    def form_valid(self, form):
        try:
            form.save(self.kwargs.get("id"))
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

class ListaSolicitudProduccionesView(PermissionRequiredMixin, TemplateView):
    permission_required = ["producciones_app.view_SolicitudProduccion"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "lista_solicitarproducciones.html"
    def get_context_data(self):
        lista = SolicitudProduccion.objects.all()
        for solicitud in lista:
            receta = Receta.objects.filter(galleta_id=solicitud.galleta_id).first()
            if receta is None:
                    solicitud.tiene_receta = False
            else:
                if receta.para_produccion is True:
                    solicitud.tiene_receta = True
                else:
                    solicitud.tiene_receta = False
        return {
            "lista": lista
        }