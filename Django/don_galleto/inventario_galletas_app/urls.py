from django.urls import path
from inventario_galletas_app.views import ListaInventarioGalletasView, mandar_a_merma
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_inventariogalletas/", login_required(ListaInventarioGalletasView.as_view()), name="lista_inventariogalletas"),
    path("mandar_a_merma/<int:pk>/", mandar_a_merma, name="mandar_a_merma"),
]