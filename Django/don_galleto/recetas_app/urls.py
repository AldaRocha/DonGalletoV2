from django.urls import path
from recetas_app.views import ListaRecetasView, CrearRecetasView, EditarRecetasView, ListaDetalleRecetaView, CrearDetalleRecetaView, EditarDetalleRecetaView, EliminarDetalleRecetaView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_recetas/", login_required(ListaRecetasView.as_view()), name="lista_recetas"),
    path("crear_recetas/", login_required(CrearRecetasView.as_view()), name="crear_recetas"),
    path("editar_recetas/<int:id>", login_required(EditarRecetasView.as_view()), name="editar_recetas"),

    path("lista_detallereceta/<int:id>", login_required(ListaDetalleRecetaView.as_view()), name="lista_detallereceta"),
    path("crear_detallereceta/<int:id>", login_required(CrearDetalleRecetaView.as_view()), name="crear_detallereceta"),
    path("editar_detallereceta/<int:id>", login_required(EditarDetalleRecetaView.as_view()), name="editar_detallereceta"),
    path("eliminar_detallereceta/<int:pk>/", login_required(EliminarDetalleRecetaView), name="detallereceta")
]
