from django.urls import path
from compras_app.views import ListaComprasView, CrearComprasView, EditarComprasView, ListaDetalleComprasView, CrearDetalleComprasView, EditarDetalleComprasView, EliminarDetalleComprasView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_compras/", login_required(ListaComprasView.as_view()), name="lista_compras"),
    path("crear_compras/", login_required(CrearComprasView.as_view()), name="crear_compras"),
    path("editar_compras/<int:id>", login_required(EditarComprasView.as_view()), name="editar_compras"),
    
    path("lista_detallecompras/<int:id>", login_required(ListaDetalleComprasView.as_view()), name="lista_detallecompras"),
    path("crear_detallecompras/<int:id>", login_required(CrearDetalleComprasView.as_view()), name="crear_detallecompras"),
    path("editar_detallecompras/<int:id>", login_required(EditarDetalleComprasView.as_view()), name="editar_detallecompras"),
    path("eliminar_detallecompras/<int:pk>/", login_required(EliminarDetalleComprasView), name="eliminar_detallecompras")
]