from django.urls import path
from ventas_app.views import ListaVenderView, agregar_al_carrito, ver_carrito, procesar_venta, eliminar_del_carrito
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("venta/", login_required(ListaVenderView.as_view()), name="venta"),
    path('agregar_al_carrito/', agregar_al_carrito, name="agregar_al_carrito"),
    path('ver_carrito/', ver_carrito, name="ver_carrito"),
    path('procesar_venta/', procesar_venta, name="procesar_venta"),
    path('eliminar_del_carrito/<str:galleta_nombre>/', eliminar_del_carrito, name="eliminar_del_carrito")
]