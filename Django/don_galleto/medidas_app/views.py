from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from medidas_app.models import Medida
from . import forms
from django.urls import reverse_lazy

# Create your views here.
class ListaMedidasView(TemplateView):
    template_name = "lista_medidas.html"
    def get_context_data(self):
        lista = Medida.objects.all()
        return {
            "lista": lista
        }

class CrearMedidasView(FormView):
    template_name = "crear_medidas.html"
    form_class = forms.MedidaRegistrarForm
    success_url = reverse_lazy("lista_medidas")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class EditarMedidasView(FormView):
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