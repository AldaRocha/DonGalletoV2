from django.urls import path
from usuarios_app.views import ListaUsuariosView, CrearUsuariosView, EditarUsuariosView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_usuarios/", login_required(ListaUsuariosView.as_view()), name="lista_usuarios"),
    path("crear_usuarios/", login_required(CrearUsuariosView.as_view()), name="crear_usuarios"),
    path("editar_usuarios/<int:id>", login_required(EditarUsuariosView.as_view()), name="editar_usuarios")
]