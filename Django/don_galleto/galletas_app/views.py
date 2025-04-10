from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from galletas_app.models import Galleta
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from producciones_app.models import SolicitudProduccion
from django.contrib import messages

# Create your views here.
class ListaGalletasView(PermissionRequiredMixin, TemplateView):
    permission_required = ["galletas_app.view_Galleta"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "lista_galletas.html"
    def get_context_data(self):
        lista = Galleta.objects.all()
        for galleta in lista:
            galleta.peso_individual = int(galleta.peso_individual)
        return {
            "lista": lista
        }

class CrearGalletasView(PermissionRequiredMixin, FormView):
    permission_required = ["galletas_app.add_Galleta"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "crear_galletas.html"
    form_class = forms.GalletaRegistrarForm
    success_url = reverse_lazy("lista_galletas")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class EditarGalletasView(PermissionRequiredMixin, FormView):
    permission_required = ["galletas_app.edit_Galleta"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "editar_galletas.html"
    form_class = forms.GalletaEditarForm
    success_url = reverse_lazy("lista_galletas")
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        galleta = get_object_or_404(Galleta, id=id)
        kwargs["instance"] = galleta
        return kwargs
    def form_valid(self, form):
        form.save(self.kwargs.get("id"))
        return super().form_valid(form)

def SolicitarGalletasView(request, pk):
    if request.method == "POST":
        galleta = get_object_or_404(Galleta, pk=pk)
        solicitud = SolicitudProduccion.objects.filter(galleta_id=galleta.id)
        if solicitud.exists():
            messages.error(request, "Ya hay una solicitud de esta galleta")
            return redirect(reverse_lazy("lista_galletas"))
        else:
            SolicitudProduccion.objects.create(
                galleta=galleta
            )
            messages.success(request, "Solicitud creada con exito")
            return redirect(reverse_lazy("lista_galletas"))
    else:
        return redirect(reverse_lazy("lista_galletas"))

def EliminarGalletaView(request, pk):
    if request.method == "POST":
        galleta = get_object_or_404(Galleta, pk=pk)
        galleta.delete()
        return redirect(reverse_lazy("lista_galletas"))
    else:
        return redirect(reverse_lazy("lista_galletas"))