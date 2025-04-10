from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from inventario_insumos_app.models import InventarioInsumos
from django.urls import reverse
from mermas_app.models import Merma
from datetime import date
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Sum

# Create your views here.

class ListaInventarioInsumosView(PermissionRequiredMixin, TemplateView):
    permission_required = ["inventario_insumos_app.view_InventarioInsumos"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "lista_inventario.html"
    def get_context_data(self, **kwargs):
        hoy = date.today()
        lista_activa = InventarioInsumos.objects.filter(activo=True)
        for insumo in lista_activa:
            if insumo.detalle_compra.fecha_caducidad.date() <= hoy:
                Merma.objects.create(
                    tipo_merma="Caducidad",
                    cantidad=insumo.cantidad_existente,
                    insumo=insumo
                )
                insumo.activo = False
                insumo.save()
        lista = (
            InventarioInsumos.objects.filter(activo=True)
            .values(
                "detalle_compra__fecha_caducidad",
                "detalle_compra__insumo__nombre",
                "detalle_compra__compra__fecha_compra",
                "detalle_compra__insumo__cantidad_minima",
                "detalle_compra__insumo__medida__nomenclatura",
            )
            .annotate(
                cantidad_existente=Sum("cantidad_existente")
            )
            .order_by("detalle_compra__fecha_caducidad")
        )
        return {
            "lista": lista
        }

def mandar_a_merma(request, pk):
    if request.method == "POST":
        insumo = get_object_or_404(InventarioInsumos, pk=pk)

        insumo.activo = False
        insumo.save()

        Merma.objects.create(
            tipo_merma="Caducidad",
            cantidad=insumo.cantidad_existente,
            insumo=insumo
        )

        return redirect(reverse("lista_inventario"))
    else:
        return redirect(reverse("lista_inventario"))