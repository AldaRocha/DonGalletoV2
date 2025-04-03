from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from compras_app.models import Compra, DetalleCompra
from . import forms
from django.urls import reverse_lazy, reverse
from decimal import Decimal

# Create your views here.
class ListaComprasView(TemplateView):
    template_name = "lista_compras.html"
    def get_context_data(self):
        lista = Compra.objects.all()
        return {
            "lista": lista
        }

class CrearComprasView(FormView):
    template_name = "crear_compras.html"
    form_class = forms.CompraRegistrarForm
    success_url = reverse_lazy("lista_compras")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class EditarComprasView(FormView):
    template_name = "editar_compras.html"
    form_class = forms.CompraEditarForm
    success_url = reverse_lazy("lista_compras")
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        compra = get_object_or_404(Compra, id=id)
        kwargs["instance"] = compra
        return kwargs
    def form_valid(self, form):
        form.save(self.kwargs.get("id"))
        return super().form_valid(form)

class ListaDetalleComprasView(TemplateView):
    template_name = "lista_detallecompras.html"
    def get_context_data(self, **kwargs):
        id = kwargs.get("id")
        lista = DetalleCompra.objects.filter(compra_id=id)
        total = Decimal("0.0")
        for detalle in lista:
            detalle.subtotal = detalle.cantidad * detalle.precio_unitario
            total += detalle.subtotal
        return {
            "lista": lista,
            "id": id,
            "total": total
        }

class CrearDetalleComprasView(FormView):
    template_name = "crear_detallecompras.html"
    form_class = forms.DetalleCompraRegistrarForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        lista = DetalleCompra.objects.filter(compra_id=id)
        total = Decimal("0.0")
        for detalle in lista:
            detalle.subtotal = detalle.cantidad * detalle.precio_unitario
            total += detalle.subtotal
        context["lista"] = lista
        context["id"] = id
        context["total"] = total
        return context
    def form_valid(self, form):
        id = self.kwargs.get("id")
        form.instance.compra_id = id
        form.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("crear_detallecompras", kwargs={"id": self.kwargs.get("id")})

class EditarDetalleComprasView(FormView):
    template_name = "editar_detallecompras.html"
    form_class = forms.DetalleCompraEditarForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        detalle = DetalleCompra.objects.filter(id=id).first()
        lista = DetalleCompra.objects.filter(compra_id=detalle.compra_id)
        total = Decimal("0.0")
        for detalle in lista:
            detalle.subtotal = detalle.cantidad * detalle.precio_unitario
            total += detalle.subtotal
        context["lista"] = lista
        context["id"] = detalle.compra_id
        context["total"] = total
        return context
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get("id")
        detallecompra = get_object_or_404(DetalleCompra, id=id)
        kwargs["instance"] = detallecompra
        return kwargs
    def form_valid(self, form):
        form.save(self.kwargs.get("id"))
        return super().form_valid(form)
    def get_success_url(self):
        id = self.kwargs.get("id")
        detalle_compra = DetalleCompra.objects.filter(id=id).first()
        return reverse("crear_detallecompras", kwargs={"id": detalle_compra.compra_id})