from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import TemplateView
from inventario_galletas_app.models import InventarioGalletas
from django.db.models import Sum, Max, F
from django.contrib import messages
from django.contrib.messages import get_messages
from django.utils.timezone import now
from ventas_app.models import Venta, DetalleVenta
from galletas_app.models import Galleta
from decimal import Decimal
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.contrib.auth.models import User

# Create your views here.
class ListaVenderView(TemplateView):
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

    detalles = []
    for producto_clave, datos in carrito.items():
        galleta_nombre, unidad = producto_clave.rsplit(" (", 1)
        unidad = unidad.rstrip(")")

        try:
            galleta = Galleta.objects.get(nombre=galleta_nombre)
        except Galleta.DoesNotExist:
            messages.error(request, f"La galleta '{galleta_nombre}' no existe.")
            continue

        cantidad_comprada = datos["cantidad"]
        if unidad == "KG":
            piezas_a_descontar = round(cantidad_comprada * (1000 / galleta.peso_individual))
        elif unidad == "Caja(s) de 12":
            piezas_a_descontar = cantidad_comprada * 12
        else:
            piezas_a_descontar = cantidad_comprada

        precio = datos["precio_maximo"]
        subtotal = cantidad_comprada * precio

        detalle = DetalleVenta.objects.create(
            cantidad=cantidad_comprada,
            precio=precio,
            subtotal=subtotal,
            galleta=galleta,
            venta=venta
        )
        detalles.append(detalle)

        inventarios = InventarioGalletas.objects.filter(produccion__galleta=galleta, cantidad__gt=0).order_by("fecha_caducidad")
        faltante = piezas_a_descontar
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

    buffer = generar_ticket(venta, detalles)
    return FileResponse(buffer, as_attachment=True, filename=f"ticket_venta_{venta.id}.pdf")

def eliminar_del_carrito(request, galleta_nombre):
    carrito = request.session.get("carrito", {})

    if galleta_nombre in carrito:
        del carrito[galleta_nombre]
        request.session["carrito"] = carrito
        messages.success(request, f"{galleta_nombre} fue eliminado del carrito.")
    else:
        messages.error(request, "El item no existe en el carrito.")

    return redirect("ver_carrito")

def generar_ticket(venta, detalles):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Ticket Venta {venta.id}")

    pdf.drawImage("static/image/logo.png", 40, 720, width=120, height=70)

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(200, 750, "")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(40, 690, f"Fecha: {venta.fecha_venta.strftime('%d-%m-%Y %H:%M')}")
    pdf.drawString(40, 670, f"ID de Venta: {venta.id}")
    pdf.drawString(40, 650, f"Usuario: {venta.usuario.username}")

    pdf.drawString(40, 620, "Detalles de la Venta:")
    x = 40
    y = 600
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(x, y, "Producto")
    pdf.drawString(x + 200, y, "Cantidad")
    pdf.drawString(x + 300, y, "Precio Unitario")
    pdf.drawString(x + 400, y, "Subtotal")

    pdf.setFont("Helvetica", 10)
    y -= 20
    total_venta = 0
    for detalle in detalles:
        pdf.drawString(x, y, detalle.galleta.nombre)
        pdf.drawString(x + 200, y, f"{detalle.cantidad}")
        pdf.drawString(x + 300, y, f"${detalle.precio:.2f}")
        pdf.drawString(x + 400, y, f"${detalle.subtotal:.2f}")
        total_venta += detalle.subtotal
        y -= 20

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y - 20, f"Total: ${total_venta:.2f}")

    pdf.save()
    buffer.seek(0)
    return buffer

def historial_ventas(request):
    if request.user.is_superuser:
        filtro_usuario_id = request.GET.get("usuario")
        usuarios = User.objects.all()

        if filtro_usuario_id:
            ventas = Venta.objects.filter(usuario_id=filtro_usuario_id)
        else:
            ventas = Venta.objects.all()
    else:
        usuarios = None
        ventas = Venta.objects.filter(usuario=request.user)

    # Calcular totales
    total_ventas = ventas.aggregate(total=Sum(F('detalleventa__cantidad') * F('detalleventa__precio')))['total'] or 0
    total_pedidos = ventas.count()
    total_galletas = ventas.aggregate(total=Sum('detalleventa__cantidad'))['total'] or 0

    return render(request, "historial_ventas.html", {
        "ventas": ventas,
        "usuarios": usuarios,
        "filtro_usuario_id": filtro_usuario_id if request.user.is_superuser else None,
        "total_ventas": total_ventas,
        "total_pedidos": total_pedidos,
        "total_galletas": total_galletas,
    })

def ver_detalles_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)

    if not request.user.is_superuser and venta.usuario != request.user:
        messages.error(request, "No tienes permiso para ver esta venta.")
        return redirect("historial_ventas")

    detalles = DetalleVenta.objects.filter(venta=venta)

    return render(request, "detalles_venta.html", {
        "venta": venta,
        "detalles": detalles
    })

def descargar_ticket(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)

    if not request.user.is_superuser and venta.usuario != request.user:
        messages.error(request, "No tienes permiso para descargar este ticket.")
        return redirect("historial_ventas")

    buffer = generar_ticket(venta, detalles)
    return FileResponse(buffer, as_attachment=True, filename=f"ticket_venta_{venta.id}.pdf")