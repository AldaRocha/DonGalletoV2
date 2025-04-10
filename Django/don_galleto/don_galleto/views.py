from django.views.generic.base import TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum, Count, F, Subquery, OuterRef, Case, When, Value, BooleanField
from django.db.models.functions import ExtractDay
from galletas_app.models import Galleta
from inventario_galletas_app.models import InventarioGalletas
from ventas_app.models import Venta, DetalleVenta
from don_galleto.forms import RegistroForm
from django.db.models import DurationField, ExpressionWrapper
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

@user_passes_test(is_admin, login_url='venta') 
def home(request):
    # Obtener fechas del filtro con valores por defecto
    fecha_fin = request.GET.get('fecha_fin')
    fecha_inicio = request.GET.get('fecha_inicio')
    
    # Si no hay fechas en el request, usar valores por defecto
    if not fecha_fin:
        fecha_fin = timezone.now().date()
    if not fecha_inicio:
        fecha_inicio = (timezone.now() - timedelta(days=30)).date()
    
    # Convertir fechas si son strings
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()

    # Ajustar las fechas para incluir todo el día
    fecha_inicio_dt = datetime.combine(fecha_inicio, datetime.min.time())
    fecha_fin_dt = datetime.combine(fecha_fin, datetime.max.time())
    
    # Aplicar timezone
    fecha_inicio_dt = timezone.make_aware(fecha_inicio_dt)
    fecha_fin_dt = timezone.make_aware(fecha_fin_dt)

    # 1. Consulta para costos de producción
    galletas = Galleta.objects.annotate(
        costo_actual=Subquery(
            InventarioGalletas.objects.filter(
                produccion__galleta=OuterRef('pk'),
                cantidad__gt=0
            ).order_by('-produccion__fecha_preparacion')
            .values('precio_por_galleta')[:1]
        ),
        ultima_actualizacion=Subquery(
            InventarioGalletas.objects.filter(
                produccion__galleta=OuterRef('pk'),
                cantidad__gt=0
            ).order_by('-produccion__fecha_preparacion')
            .values('produccion__fecha_preparacion')[:1]
        ),
        total_insumos=Count('receta__detallereceta', distinct=True)
    ).filter(costo_actual__isnull=False)

    # 2. Consulta para galletas por antigüedad de producción
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
            When(tiempo_desde_produccion__gte=timedelta(hours=2), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    ).filter(es_urgente=True).order_by('produccion__fecha_preparacion')

    # 3. Estadísticas de ventas
    ventas_filtradas = Venta.objects.filter(
        fecha_venta__gte=fecha_inicio_dt,
        fecha_venta__lte=fecha_fin_dt
    )
    
    # Calcular totales de ventas
    detalles_ventas = DetalleVenta.objects.filter(
        venta__in=ventas_filtradas
    )
    
    total_ventas = detalles_ventas.aggregate(
        total=Sum(F('cantidad') * F('precio'))
    )['total'] or 0
    
    total_pedidos = ventas_filtradas.count()
    
    total_galletas = detalles_ventas.aggregate(
        total=Sum('cantidad')
    )['total'] or 0

    # 4. Ventas por tipo de galleta
    ventas_por_galleta = DetalleVenta.objects.filter(
        venta__in=ventas_filtradas
    ).values(
        'galleta__nombre'
    ).annotate(
        cantidad_total=Sum('cantidad'),
        total_ventas=Sum(F('cantidad') * F('precio'))
    ).order_by('-total_ventas')

    context = {
        'galletas': galletas,
        'galletas_por_produccion': galletas_por_produccion,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total_ventas': total_ventas,
        'total_pedidos': total_pedidos,
        'total_galletas': total_galletas,
        'ventas_por_galleta': ventas_por_galleta,
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