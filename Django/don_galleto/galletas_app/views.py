from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from galletas_app.models import Galleta
from . import forms
from django.urls import reverse_lazy

# Create your views here.
class ListaGalletasView(TemplateView):
    template_name = "lista_galletas.html"
    def get_context_data(self):
        lista = Galleta.objects.all()
        return {
            "lista": lista
        }

class CrearGalletasView(FormView):
    template_name = "crear_galletas.html"
    form_class = forms.GalletaRegistrarForm
    success_url = reverse_lazy("lista_galletas")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class EditarGalletasView(FormView):
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

def EliminarGalletaView(request, pk):
    if request.method == "POST":
        galleta = get_object_or_404(Galleta, pk=pk)
        galleta.delete()
        return redirect(reverse_lazy("lista_galletas"))
    else:
        return redirect(reverse_lazy("lista_galletas"))