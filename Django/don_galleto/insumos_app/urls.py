from django.urls import path
from insumos_app.views import ListaInsumosView, CrearInsumosView, EditarInsumosView, EliminarInsumoView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_insumos/", login_required(ListaInsumosView.as_view()), name="lista_insumos"),
    path("crear_insumos/", login_required(CrearInsumosView.as_view()), name="crear_insumos"),
    path("editar_insumos/<int:id>", login_required(EditarInsumosView.as_view()), name="editar_insumos"),
    path("eliminar_insumos/<int:pk>/", login_required(EliminarInsumoView), name="eliminar_insumos")
]