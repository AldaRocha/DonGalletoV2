"""
URL configuration for don_galleto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from . import views
from usuarios_app.views import check_availability

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('cuentas/registro', views.registro, name="registro"),
    path('home', login_required(views.home), name='home'),
    path('usuarios/', include('usuarios_app.urls')),
    path('proveedores/', include('proveedores_app.urls')),
    path('medidas/', include('medidas_app.urls')),
    path('insumos/', include('insumos_app.urls')),
    path('compras/', include('compras_app.urls')),
    path('inventario_insumos/', include('inventario_insumos_app.urls')),
    path('galletas/', include('galletas_app.urls')),
    path('recetas/', include('recetas_app.urls')),
    path('producciones/', include('producciones_app.urls')),
    path('mermas/', include('mermas_app.urls')),
    path('inventario_galletas/', include('inventario_galletas_app.urls')),
    path('check-availability/', check_availability, name='check_availability'),
    path('ventas/', include('ventas_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = views.custom_404
handler500 = views.custom_500