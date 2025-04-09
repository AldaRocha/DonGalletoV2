from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from recetas_app.models import Receta, DetalleReceta
from . import forms
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
class ListaRecetasView(PermissionRequiredMixin, TemplateView):
    permission_required = ["recetas_app.view_Receta"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("home")
    template_name = "lista_recetas.html"
    def get_context_data(self):
        lista = Receta.objects.all()
        for receta in lista:
            receta.para_produccion = "Si" if receta.para_produccion else "No"
        return {
            "lista": lista
        }

class CrearRecetasView(PermissionRequiredMixin, FormView):
    permission_required = ["recetas_app.add_Receta"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("home")
    template_name = "crear_recetas.html"
    form_class = forms.RecetaRegistrarForm
    success_url = reverse_lazy("lista_recetas")
    def form_valid(self, form):
        try:
            form.save()
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

class EditarRecetasView(PermissionRequiredMixin, FormView):
    permission_required = ["recetas_app.edit_Receta"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("home")
    template_name = "editar_recetas.html"
    form_class = forms.RecetaEditarForm
    success_url = reverse_lazy("lista_recetas")
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        receta = get_object_or_404(Receta, id=id)
        kwargs["instance"] = receta
        return kwargs
    def form_valid(self, form):
        try:
            form.save(self.kwargs.get("id"))
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

class ListaDetalleRecetaView(PermissionRequiredMixin, TemplateView):
    permission_required = ["recetas_app.view_DetalleReceta"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("home")
    template_name = "lista_detallereceta.html"
    def get_context_data(self, **kwargs):
        id = kwargs.get("id")
        lista = DetalleReceta.objects.filter(receta_id=id)
        return {
            "lista": lista,
            "id": id
        }

class CrearDetalleRecetaView(PermissionRequiredMixin, FormView):
    permission_required = ["recetas_app.add_DetalleReceta"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("home")
    template_name = "crear_detallereceta.html"
    form_class = forms.DetalleRecetaRegistrarForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        lista = DetalleReceta.objects.filter(receta_id=id)
        context["lista"] = lista
        context["id"] = id
        return context
    def form_valid(self, form):
        id = self.kwargs.get("id")
        form.instance.receta_id = id
        form.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("crear_detallereceta", kwargs={"id": self.kwargs.get("id")})

class EditarDetalleRecetaView(PermissionRequiredMixin, FormView):
    permission_required = ["recetas_app.edit_DetalleReceta"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("home")
    template_name = "editar_detallereceta.html"
    form_class = forms.DetalleRecetaEditarForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        detalle = DetalleReceta.objects.filter(id=id).first()
        lista = DetalleReceta.objects.filter(receta_id=detalle.receta_id)
        context["lista"] = lista
        context["id"] = detalle.receta_id
        return context
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        detallereceta = get_object_or_404(DetalleReceta, id=id)
        kwargs["instance"] = detallereceta
        return kwargs
    def form_valid(self, form):
        form.save(self.kwargs.get("id"))
        return super().form_valid(form)
    def get_success_url(self):
        id = self.kwargs.get("id")
        detalle_receta = DetalleReceta.objects.filter(id=id).first()
        return reverse("crear_detallereceta", kwargs={"id": detalle_receta.receta_id})

def EliminarDetalleRecetaView(request, pk):
    if request.method == "POST":
        detalle_receta = get_object_or_404(DetalleReceta, pk=pk)
        receta_id = detalle_receta.receta_id
        detalle_receta.delete()
        return redirect(reverse("lista_detallereceta", kwargs={"id": receta_id}))
    else:
        return redirect(reverse_lazy("lista_recetas"))