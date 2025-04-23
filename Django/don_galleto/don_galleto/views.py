from django.views.generic.base import TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import (
    Sum, Count, F, Subquery, OuterRef, Case, 
    When, Value, BooleanField
)
from django.db.models.functions import ExtractDay, Coalesce  # Added Coalesce here
from galletas_app.models import Galleta
from inventario_galletas_app.models import InventarioGalletas
from ventas_app.models import Venta, DetalleVenta
from don_galleto.forms import RegistroForm
from django.db.models import DurationField, ExpressionWrapper
from django.utils.timezone import now
from django.contrib.auth.decorators import user_passes_test
from decimal import Decimal, ROUND_HALF_UP
from recetas_app.models import Receta

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

@user_passes_test(is_admin, login_url='venta') 
def home(request):
    try:
        # Obtener y validar fechas
        fecha_fin = request.GET.get('fecha_fin')
        fecha_inicio = request.GET.get('fecha_inicio')
        
        if not fecha_fin:
            fecha_fin = timezone.now().date()
        if not fecha_inicio:
            fecha_inicio = (timezone.now() - timedelta(days=30)).date()
        
        if isinstance(fecha_fin, str):
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        if isinstance(fecha_inicio, str):
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()

        fecha_inicio_dt = timezone.make_aware(datetime.combine(fecha_inicio, datetime.min.time()))
        fecha_fin_dt = timezone.make_aware(datetime.combine(fecha_fin, datetime.max.time()))

        # 1. Consulta para galletas y sus costos
        galletas = Galleta.objects.all().prefetch_related(
            'receta_set'
        ).order_by('nombre')

        # 2. Estadísticas de ventas del período
        ventas_filtradas = Venta.objects.filter(
            fecha_venta__gte=fecha_inicio_dt,
            fecha_venta__lte=fecha_fin_dt
        )
        
        detalles_ventas = DetalleVenta.objects.filter(
            venta__in=ventas_filtradas
        ).select_related('galleta')

        # Calcular totales
        total_ventas = detalles_ventas.aggregate(
            total=Coalesce(Sum(F('cantidad') * F('precio')), Decimal('0'))
        )['total']
        
        total_pedidos = ventas_filtradas.count()
        
        total_galletas_vendidas = detalles_ventas.aggregate(
            total=Coalesce(Sum('cantidad'), 0)
        )['total']

        # 3. Ventas por galleta
        ventas_por_galleta = detalles_ventas.values(
            'galleta__nombre'
        ).annotate(
            cantidad_total=Coalesce(Sum('cantidad'), 0),
            total_ventas=Coalesce(Sum(F('cantidad') * F('precio')), Decimal('0'))
        ).order_by('-total_ventas')

        # 4. Estado de producción
        galletas_por_produccion = InventarioGalletas.objects.filter(
            cantidad__gt=0
        ).select_related(
            'produccion__galleta'
        ).annotate(
            tiempo_desde_produccion=ExpressionWrapper(
                now() - F('produccion__fecha_preparacion'),
                output_field=DurationField()
            ),
            es_urgente=Case(
                When(tiempo_desde_produccion__gte=timedelta(hours=48), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).order_by('produccion__fecha_preparacion')

        context = {
            'galletas': galletas,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total_ventas': total_ventas,
            'total_pedidos': total_pedidos,
            'total_galletas': total_galletas_vendidas,
            'ventas_por_galleta': ventas_por_galleta,
            'galletas_por_produccion': galletas_por_produccion,
        }

        return render(request, 'home.html', context)
        
    except Exception as e:
        print(f"Error en home view: {e}")
        context = {
            'galletas': Galleta.objects.none(),
            'fecha_inicio': timezone.now().date() - timedelta(days=30),
            'fecha_fin': timezone.now().date(),
            'total_ventas': Decimal('0.00'),
            'total_pedidos': 0,
            'total_galletas': 0,
            'ventas_por_galleta': [],
            'galletas_por_produccion': [],
        }
        return render(request, 'home.html', context)

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegistroForm()
    return render(request, "registration/registro.html", {"form": form})

def custom_404(request, excepction):
    return render(request, "404.html", status=404)

def custom_500(request):
    return render(request, "500.html")