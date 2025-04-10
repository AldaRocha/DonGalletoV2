from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from inventario_galletas_app.models import InventarioGalletas
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Sum, Max
from django.contrib import messages
from django.contrib.messages import get_messages
from django.utils.timezone import now
from ventas_app.models import Venta, DetalleVenta
from galletas_app.models import Galleta
from decimal import Decimal

# Create your views here.
class ListaVenderView(PermissionRequiredMixin, TemplateView):
    permission_required = ["ventas_app.view_Venta"]
    login_url = "login"
    template_name = "venta.html"

    def get_context_data(self, **kwargs):
        unidad = self.request.GET.get("unidad", "pz")

        lista = (
            InventarioGalletas.objects.filter(cantidad__gt=0)
            .values(
                "produccion__galleta__nombre",
                "produccion__galleta__descripcion",
                "produccion__galleta__imagen",
                "produccion__galleta__peso_individual"
            )
            .annotate(
                total_cantidad=Sum("cantidad"),
                precio_maximo=Max("precio_por_galleta")
            )
            .order_by("produccion__galleta")
        )

        for item in lista:
            if unidad == "kg":
                peso_kg = Decimal(item["produccion__galleta__peso_individual"]) / Decimal(1000)
                item["existencia"] = round(Decimal(item["total_cantidad"]) * peso_kg, 2)
                item["precio_maximo"] = item["precio_maximo"] * round(1000 / item["produccion__galleta__peso_individual"], 2)
                item["unidad"] = "KG"
            elif unidad == "caja":
                item["existencia"] = item["total_cantidad"] // 12
                item["precio_maximo"] = item["precio_maximo"] * 12
                item["unidad"] = "Caja(s) de 12"
            else:
                item["existencia"] = item["total_cantidad"]
                item["precio_maximo"] = item["precio_maximo"]
                item["unidad"] = "PZ"

        return {
            "lista": lista,
            "unidad_actual": unidad
        }

def agregar_al_carrito(request):
    if request.method == "POST":
        storage = get_messages(request)
        for _ in storage:
            pass

        galleta_nombre = request.POST.get("galleta_nombre")
        cantidad = int(request.POST.get("cantidad"))
        unidad = request.POST.get("unidad")

        precio_maximo_raw = request.POST.get("precio_maximo")
        precio_maximo = float(precio_maximo_raw.replace(",", "."))

        carrito = request.session.get("carrito", {})

        producto_clave = f"{galleta_nombre} ({unidad})"

        if producto_clave in carrito:
            carrito[producto_clave]["cantidad"] += cantidad
        else:
            carrito[producto_clave] = {
                "cantidad": cantidad,
                "precio_maximo": precio_maximo,
                "unidad": unidad
            }

        request.session["carrito"] = carrito
        messages.success(request, f"{cantidad} unidad(es) de {producto_clave} agregadas al carrito.")
        return redirect("venta")

def ver_carrito(request):
    carrito = request.session.get("carrito", {})
    carrito_con_totales = []

    total_venta = 0.00
    for producto_clave, datos in carrito.items():
        total = datos["cantidad"] * datos["precio_maximo"]
        total_venta += total
        carrito_con_totales.append({
            "nombre": producto_clave,
            "cantidad": datos["cantidad"],
            "precio_maximo": datos["precio_maximo"],
            "total": total,
            "unidad": datos["unidad"]
        })

    return render(request, "carrito.html", {"carrito": carrito_con_totales, "total": total_venta})

def procesar_venta(request):
    carrito = request.session.get("carrito", {})

    if not carrito:
        messages.error(request, "El carrito está vacío. Agrega productos antes de proceder.")
        return redirect("venta")

    venta = Venta.objects.create(
        fecha_venta=now(),
        usuario=request.user
    )

    for producto_clave, datos in carrito.items():
        galleta_nombre, unidad = producto_clave.rsplit(" (", 1)
        unidad = unidad.rstrip(")")

        try:
            galleta = Galleta.objects.get(nombre=galleta_nombre)
        except Galleta.DoesNotExist:
            messages.error(request, f"La galleta '{galleta_nombre}' no existe.")
            continue

        cantidad_comprada = datos["cantidad"]
        print(f"g: {unidad}")
        if unidad == "KG":
            piezas_a_descontar = round(cantidad_comprada * (1000 / galleta.peso_individual))
        elif unidad == "Caja(s) de 12":
            piezas_a_descontar = cantidad_comprada * 12
        else:
            piezas_a_descontar = cantidad_comprada

        precio = datos["precio_maximo"]
        subtotal = cantidad_comprada * precio

        DetalleVenta.objects.create(
            cantidad=cantidad_comprada,
            precio=precio,
            subtotal=subtotal,
            galleta=galleta,
            venta=venta
        )

        inventarios = InventarioGalletas.objects.filter(produccion__galleta=galleta, cantidad__gt=0).order_by("fecha_caducidad")
        faltante = piezas_a_descontar
        print(faltante)
        for inventario in inventarios:
            if faltante <= 0:
                break
            if inventario.cantidad >= faltante:
                inventario.cantidad -= faltante
                if inventario.cantidad == 0:
                    inventario.delete()
                else:
                    inventario.save()
                faltante = 0
            else:
                faltante -= inventario.cantidad
                inventario.delete()

    request.session["carrito"] = {}

    messages.success(request, "La venta se procesó exitosamente.")
    return redirect("venta")

def eliminar_del_carrito(request, galleta_nombre):
    carrito = request.session.get("carrito", {})

    if galleta_nombre in carrito:
        del carrito[galleta_nombre]
        request.session["carrito"] = carrito
        messages.success(request, f"{galleta_nombre} fue eliminado del carrito.")
    else:
        messages.error(request, "El item no existe en el carrito.")

    return redirect("ver_carrito")