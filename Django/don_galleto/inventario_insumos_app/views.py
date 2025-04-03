from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from inventario_insumos_app.models import InventarioInsumos
from . import forms
from django.urls import reverse_lazy

# Create your views here.
class ListaInventarioInsumosView(TemplateView):
    template_name = "lista_inventario.html"
    def get_context_data(self):
        lista = InventarioInsumos.objects.all()
        return {
            "lista": lista
        }

class CrearInventarioInsumosView(FormView):
    template_name = "crear_inventario.html"
    form_class = forms.InventarioInsumosRegistrarForm
    success_url = reverse_lazy("lista_inventario")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class EditarInventarioInsumosView(FormView):
    template_name = "editar_inventario.html"
    form_class = forms.InventarioInsumosEditarForm
    success_url = reverse_lazy("lista_inventario")
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        inventarioInsumos = get_object_or_404(InventarioInsumos, id=id)
        kwargs["instance"] = inventarioInsumos
        return kwargs
    def form_valid(self, form):
        form.save(self.kwargs.get("id"))
        return super().form_valid(form)