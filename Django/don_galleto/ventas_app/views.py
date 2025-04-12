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
from django.db import transaction
from decimal import Decimal, InvalidOperation, DecimalException 

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
            # Guarda siempre el precio original por pieza
            precio_original = item["precio_maximo"]
            
            if unidad == "kg":
                peso_kg = Decimal(item["produccion__galleta__peso_individual"]) / Decimal(1000)
                item["existencia"] = round(Decimal(item["total_cantidad"]) * peso_kg, 2)
                item["precio_maximo"] = precio_original * round(1000 / item["produccion__galleta__peso_individual"], 2)
                item["unidad"] = "KG"
            elif unidad == "caja":
                item["existencia"] = item["total_cantidad"] // 12
                item["precio_maximo"] = precio_original * 12
                item["unidad"] = "Caja(s) de 12"
            else:
                item["existencia"] = item["total_cantidad"]
                item["precio_maximo"] = precio_original
                item["unidad"] = "PZ"
                
            # Este precio siempre será el que aparece en pantalla y usamos en el carrito
            item["precio_para_carrito"] = item["precio_maximo"]

        return {
            "lista": lista,
            "unidad_actual": unidad
        }

def agregar_al_carrito(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                galleta_nombre = request.POST.get("galleta_nombre")
                cantidad = int(request.POST.get("cantidad"))
                unidad = request.POST.get("unidad")
                
                # En lugar de obtener precio del POST, obtenerlo directamente de la base de datos
                # para evitar todos los problemas de formato
                
                # Buscar la galleta en el inventario
                inventario = InventarioGalletas.objects.filter(
                    produccion__galleta__nombre=galleta_nombre,
                    cantidad__gt=0
                ).order_by('produccion__fecha_preparacion').first()

                if not inventario or inventario.cantidad < cantidad:
                    messages.error(request, "No hay suficiente stock disponible")
                    return redirect('venta')
                
                # Obtener el precio directamente de la base de datos
                galleta = inventario.produccion.galleta
                precio_base = inventario.precio_por_galleta
                
                # Ajustar precio según unidad
                if unidad == "KG":
                    precio_unitario = precio_base * (1000 / galleta.peso_individual)
                elif unidad == "Caja(s) de 12":
                    precio_unitario = precio_base * 12
                else:
                    precio_unitario = precio_base
                
                # Actualizar inventario
                inventario.cantidad = F('cantidad') - cantidad
                inventario.save()
                inventario.refresh_from_db()

                # Calcular total
                total = precio_unitario * Decimal(str(cantidad))

                # Preparar carrito
                carrito = request.session.get('carrito', [])
                if not isinstance(carrito, list):
                    carrito = []

                carrito.append({
                    'galleta': galleta_nombre,
                    'cantidad': cantidad,
                    'precio': str(precio_unitario),
                    'unidad': unidad,
                    'total': str(total),
                    'inventario_id': inventario.id
                })
                request.session['carrito'] = carrito
                messages.success(request, "Producto agregado al carrito")
                return redirect('venta')

        except ValueError as ve:
            messages.error(request, str(ve))
            return redirect('venta')
        except Exception as e:
            messages.error(request, f"Error al agregar al carrito: {str(e)}")
            return redirect('venta')
        
def ver_carrito(request):
    carrito = request.session.get("carrito", [])
    carrito_con_totales = []
    total_venta = Decimal('0.00')

    for item in carrito:
        precio = Decimal(item['precio'])  # Usar el precio tal como está
        cantidad = item['cantidad']
        unidad = item['unidad']
        total = Decimal(item['total'])  
        total_venta += total
        
        carrito_con_totales.append({
            "nombre": item['galleta'],
            "cantidad": cantidad,
            "precio_maximo": str(precio),  # Mostrar el precio tal como está
            "total": str(total),
            "unidad": unidad
        })

    return render(request, "carrito.html", {
        "carrito": carrito_con_totales, 
        "total": total_venta
    })

@transaction.atomic
def procesar_venta(request):
    try:
        carrito = request.session.get("carrito", [])

        if not carrito:
            messages.error(request, "El carrito está vacío. Agrega productos antes de proceder.")
            return redirect("venta")

        # Create sale in a transaction
        venta = Venta.objects.create(
            fecha_venta=now(),
            usuario=request.user
        )

        detalles = []
        for item in carrito:
            galleta_nombre = item['galleta']
            cantidad = item['cantidad']
            precio = Decimal(item['precio'])
            unidad = item['unidad']
            inventario_id = item['inventario_id']

            try:
                galleta = Galleta.objects.get(nombre=galleta_nombre)
            except Galleta.DoesNotExist:
                raise ValueError(f"La galleta '{galleta_nombre}' no existe.")

            # Calculate pieces to discount based on unit
            if unidad == "KG":
                piezas_a_descontar = round(cantidad * (1000 / galleta.peso_individual))
            elif unidad == "Caja(s) de 12":
                piezas_a_descontar = cantidad * 12
            else:
                piezas_a_descontar = cantidad

            # Create sale detail
            detalle = DetalleVenta.objects.create(
                cantidad=cantidad,
                precio=precio,
                subtotal=Decimal(item['total']),
                galleta=galleta,
                venta=venta
            )
            detalles.append(detalle)

            # Verify and update inventory
            try:
                inventario = InventarioGalletas.objects.get(
                    id=inventario_id,
                    cantidad__gte=piezas_a_descontar
                )
                inventario.cantidad -= piezas_a_descontar
                if inventario.cantidad == 0:
                    inventario.delete()
                else:
                    inventario.save()
            except InventarioGalletas.DoesNotExist:
                raise ValueError(f"No hay suficiente inventario para {galleta_nombre}")

        # Limpiar carrito
        request.session["carrito"] = []
        
        # Agregar mensaje de éxito
        messages.success(request, "Venta realizada con éxito")
        
        # Generar y descargar ticket, luego redirigir
        buffer = generar_ticket(venta, detalles)
        response = FileResponse(buffer, as_attachment=True, filename=f"ticket_venta_{venta.id}.pdf")
        return response

    except ValueError as ve:
        messages.error(request, str(ve))
        return redirect("ver_carrito")
    except Exception as e:
        messages.error(request, f"Error al procesar la venta: {str(e)}")
        return redirect("ver_carrito")

def eliminar_del_carrito(request, galleta_nombre):
    try:
        with transaction.atomic():
            carrito = request.session.get("carrito", [])
            
            # Find and remove the item from cart
            for item in carrito[:]:  # Create a copy to iterate
                if item['galleta'] == galleta_nombre:
                    # Restore inventory
                    inventario = InventarioGalletas.objects.get(id=item['inventario_id'])
                    inventario.cantidad = F('cantidad') + item['cantidad']
                    inventario.save()
                    
                    carrito.remove(item)
                    messages.success(request, f"{galleta_nombre} fue eliminado del carrito.")
                    break
            else:
                messages.error(request, "El item no existe en el carrito.")

            request.session["carrito"] = carrito
            
    except Exception as e:
        messages.error(request, f"Error al eliminar del carrito: {str(e)}")
    
    return redirect("ver_carrito")

def cancelar_carrito(request):
    try:
        with transaction.atomic():
            carrito = request.session.get("carrito", [])
            
            # Restore inventory for all items
            for item in carrito:
                if 'inventario_id' in item:
                    inventario = InventarioGalletas.objects.get(id=item['inventario_id'])
                    inventario.cantidad = F('cantidad') + item['cantidad']
                    inventario.save()
            
            # Clear cart
            request.session["carrito"] = []
            messages.success(request, "Carrito cancelado correctamente")
            
    except Exception as e:
        messages.error(request, f"Error al cancelar el carrito: {str(e)}")
    
    return redirect("venta")

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