from django.urls import path
from inventario_insumos_app.views import ListaInventarioInsumosView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_inventario/", login_required(ListaInventarioInsumosView.as_view()), name="lista_inventario")
]