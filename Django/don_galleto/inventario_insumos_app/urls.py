from django.urls import path
from inventario_insumos_app.views import ListaInventarioInsumosView, mandar_a_merma
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_inventario/", login_required(ListaInventarioInsumosView.as_view()), name="lista_inventario"),
    path("mandar_a_merma/<int:pk>/", mandar_a_merma, name="mandar_a_merma"),
]