from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from inventario_galletas_app.models import InventarioGalletas
from django.urls import reverse
from mermas_app.models import Merma
from datetime import date
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
class ListaInventarioGalletasView(PermissionRequiredMixin, TemplateView):
    permission_required = ["inventario_galletas_app.view_InventarioGalletas"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "lista_inventariogalletas.html"
    def get_context_data(self):
        hoy = date.today()
        lista_activa = InventarioGalletas.objects.all()
        for galleta in lista_activa:
            if galleta.fecha_caducidad.date() <= hoy:
                Merma.objects.create(
                    tipo_merma="Caducidad",
                    cantidad=galleta.cantidad,
                    produccion=galleta.produccion
                )
                galleta.delete()
        lista = InventarioGalletas.objects.filter(cantidad__gt=0)
        return {
            "lista": lista
        }

def mandar_a_merma(request, pk):
    if request.method == "POST":
        galletas = get_object_or_404(InventarioGalletas, pk=pk)

        merma = galletas.cantidad
        galletas.cantidad = 0
        galletas.save()

        Merma.objects.create(
            tipo_merma="Caducidad",
            cantidad=merma,
            produccion=galletas.produccion
        )

        return redirect(reverse("lista_inventariogalletas"))
    else:
        return redirect(reverse("lista_inventariogalletas"))