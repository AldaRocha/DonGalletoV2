from django.urls import path
from proveedores_app.views import ListaProveedoresView, CrearProveedoresView, EditarProveedoresView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_proveedores/", login_required(ListaProveedoresView.as_view()), name="lista_proveedores"),
    path("crear_proveedores/", login_required(CrearProveedoresView.as_view()), name="crear_proveedores"),
    path("editar_proveedores/<int:id>", login_required(EditarProveedoresView.as_view()), name="editar_proveedores")
]