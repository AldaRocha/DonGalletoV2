from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from producciones_app.models import Produccion
from . import forms
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError

# Create your views here.
class ListaProduccionesView(TemplateView):
    template_name = "lista_producciones.html"
    def get_context_data(self):
        lista = Produccion.objects.all()
        return {
            "lista": lista
        }

class CrearProduccionesView(FormView):
    template_name = "crear_producciones.html"
    form_class = forms.ProduccionRegistrarForm
    success_url = reverse_lazy("lista_producciones")
    def form_valid(self, form):
        try:
            form.save()
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

class EditarProduccionesView(FormView):
    template_name = "editar_producciones.html"
    form_class = forms.ProduccionEditarForm
    success_url = reverse_lazy("lista_producciones")
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        produccion = get_object_or_404(Produccion, id=id)
        kwargs["instance"] = produccion
        return kwargs
    def form_valid(self, form):
        try:
            form.save(self.kwargs.get("id"))
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)
