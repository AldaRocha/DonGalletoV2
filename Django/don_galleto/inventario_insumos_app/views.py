from django.views.generic.base import TemplateView
from inventario_insumos_app.models import InventarioInsumos

# Create your views here.
class ListaInventarioInsumosView(TemplateView):
    template_name = "lista_inventario.html"
    def get_context_data(self):
        lista = InventarioInsumos.objects.filter(activo=True)
        return {
            "lista": lista
        }