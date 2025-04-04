from django.urls import path
from galletas_app.views import ListaGalletasView, CrearGalletasView, EditarGalletasView, EliminarGalletaView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_galletas/", login_required(ListaGalletasView.as_view()), name="lista_galletas"),
    path("crear_galletas/", login_required(CrearGalletasView.as_view()), name="crear_galletas"),
    path("editar_galletas/<int:id>", login_required(EditarGalletasView.as_view()), name="editar_galletas"),
    path("eliminar_galletas/<int:pk>/", login_required(EliminarGalletaView), name="eliminar_galletas")
]