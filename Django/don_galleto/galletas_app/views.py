from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from galletas_app.models import Galleta
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from producciones_app.models import SolicitudProduccion
from django.contrib import messages
from decimal import Decimal, ROUND_HALF_UP
from django.views.generic import UpdateView

# Create your views here.
class ListaGalletasView(PermissionRequiredMixin, TemplateView):
    permission_required = ["galletas_app.view_Galleta"]
    login_url = "login"
    template_name = "lista_galletas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        galletas = Galleta.objects.all().prefetch_related('receta_set')
        context['lista'] = galletas
        return context

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

class EditarGalletasView(PermissionRequiredMixin, UpdateView):
    permission_required = ["galletas_app.change_galleta"]  # Nota: cambié edit_Galleta a change_galleta
    model = Galleta
    login_url = "login"
    template_name = "editar_galletas.html"
    form_class = forms.GalletaEditarForm
    success_url = reverse_lazy("lista_galletas")
    pk_url_kwarg = 'id'  # Para que coincida con el parámetro que estás usando en la URL

    def form_valid(self, form):
        # Guardar el formulario
        response = super().form_valid(form)
        
        # Actualizar el precio de producción
        self.object.precio_produccion = Decimal(str(self.object.precio_produccion_actual)).quantize(
            Decimal('0.01'), 
            rounding=ROUND_HALF_UP
        )
        self.object.save()
        
        messages.success(self.request, "Galleta actualizada exitosamente")
        return response

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