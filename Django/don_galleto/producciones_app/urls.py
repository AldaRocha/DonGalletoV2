from django.urls import path
from producciones_app.views import ListaProduccionesView, CrearProduccionesView, EditarProduccionesView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_producciones/", login_required(ListaProduccionesView.as_view()), name="lista_producciones"),
    path("crear_producciones/", login_required(CrearProduccionesView.as_view()), name="crear_producciones"),
    path("editar_producciones/<int:id>", login_required(EditarProduccionesView.as_view()), name="editar_producciones")
]
