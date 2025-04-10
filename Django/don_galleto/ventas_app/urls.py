from django.urls import path
from ventas_app.views import ListaVenderView, agregar_al_carrito, ver_carrito, procesar_venta, eliminar_del_carrito, historial_ventas, ver_detalles_venta, descargar_ticket
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("venta/", login_required(ListaVenderView.as_view()), name="venta"),
    path('agregar_al_carrito/', agregar_al_carrito, name="agregar_al_carrito"),
    path('ver_carrito/', ver_carrito, name="ver_carrito"),
    path('procesar_venta/', procesar_venta, name="procesar_venta"),
    path('eliminar_del_carrito/<str:galleta_nombre>/', eliminar_del_carrito, name="eliminar_del_carrito"),
    path('historial_ventas/', historial_ventas, name="filtrar_historial"),
    path('ver_detalles_venta/<int:venta_id>/', ver_detalles_venta, name="ver_detalles_venta"),
    path('descargar_ticket/<int:venta_id>/', descargar_ticket, name="descargar_ticket")
]