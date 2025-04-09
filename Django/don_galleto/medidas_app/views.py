from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from medidas_app.models import Medida
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
class ListaMedidasView(PermissionRequiredMixin, TemplateView):
    permission_required = ["medidas_app.view_Medida"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("home")
    template_name = "lista_medidas.html"
    def get_context_data(self):
        lista = Medida.objects.all()
        return {
            "lista": lista
        }

class CrearMedidasView(PermissionRequiredMixin, FormView):
    permission_required = ["medidas_app.add_Medida"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("home")
    template_name = "crear_medidas.html"
    form_class = forms.MedidaRegistrarForm
    success_url = reverse_lazy("lista_medidas")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class EditarMedidasView(PermissionRequiredMixin, FormView):
    permission_required = ["medidas_app.edit_Medida"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("home")
    template_name = "editar_medidas.html"
    form_class = forms.MedidaEditarForm
    success_url = reverse_lazy("lista_medidas")
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        medida = get_object_or_404(Medida, id=id)
        kwargs["instance"] = medida
        return kwargs
    def form_valid(self, form):
        form.save(self.kwargs.get("id"))
        return super().form_valid(form)