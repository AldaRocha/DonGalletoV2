from django.urls import path
from .views import (
    CrearProveedorView,
    ListaProveedoresView,
    EditarProveedorView,
    CrearInsumoView,
    ListaInsumosView,
    CrearCompraView,
    ListaComprasView,
    RegistrarMermaView,
    ListaMermasView,
)

urlpatterns = [
    path('crear_proveedor/', CrearProveedorView.as_view(), name='crear_proveedor'),
    path('lista_proveedores/', ListaProveedoresView.as_view(), name='lista_proveedores'),
    path('editar_proveedor/<int:pk>/', EditarProveedorView.as_view(), name='editar_proveedor'),
    path('crear_insumo/', CrearInsumoView.as_view(), name='crear_insumo'),
    path('lista_insumos/', ListaInsumosView.as_view(), name='lista_insumos'),
    path('crear_compra/', CrearCompraView.as_view(), name='crear_compra'),
    path('lista_compras/', ListaComprasView.as_view(), name='lista_compras'),
    path('registrar_merma/', RegistrarMermaView.as_view(), name='registrar_merma'),
    path('lista_mermas/', ListaMermasView.as_view(), name='lista_mermas'),
]
