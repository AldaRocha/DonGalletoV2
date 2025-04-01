from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from insumos_app.models import Insumo
from . import forms
from django.urls import reverse_lazy

# Create your views here.
class ListaInsumosView(TemplateView):
    template_name = "lista_insumos.html"
    def get_context_data(self):
        lista = Insumo.objects.all()
        return {
            "lista": lista
        }

class CrearInsumosView(FormView):
    template_name = "crear_insumos.html"
    form_class = forms.InsumoRegistrarForm
    success_url = reverse_lazy("lista_insumos")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class EditarInsumosView(FormView):
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