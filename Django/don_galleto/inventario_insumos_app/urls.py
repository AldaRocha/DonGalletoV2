from django.urls import path
from inventario_insumos_app.views import ListaInventarioInsumosView, CrearInventarioInsumosView, EditarInventarioInsumosView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_inventario/", login_required(ListaInventarioInsumosView.as_view()), name="lista_inventario"),
    path("crear_inventario/", login_required(CrearInventarioInsumosView.as_view()), name="crear_inventario"),
    path("editar_inventario/<int:id>", login_required(EditarInventarioInsumosView.as_view()), name="editar_inventario")
]