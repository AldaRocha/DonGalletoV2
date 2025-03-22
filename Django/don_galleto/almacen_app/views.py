from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from .models import Proveedor, Insumo, Compra, Merma
from .forms import ProveedorForm, InsumoForm, CompraForm, MermaForm

# Vista para listar los insumos
class ListaInsumosView(ListView):
    model = Insumo
    template_name = 'almacen/lista_insumos.html'
    context_object_name = 'insumos'

# Vista para crear un insumo
class CrearInsumoView(CreateView):
    model = Insumo
    form_class = InsumoForm
    template_name = 'almacen/crear_insumo.html'
    success_url = reverse_lazy('lista_insumos')

# Vista para crear un proveedor
class CrearProveedorView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'almacen/crear_proveedor.html'
    success_url = reverse_lazy('lista_proveedores')

# Vista para editar un proveedor
class EditarProveedorView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'almacen/editar_proveedor.html'
    success_url = reverse_lazy('lista_proveedores')

# Vista para listar las compras
class ListaComprasView(ListView):
    model = Compra
    template_name = 'almacen/lista_compras.html'
    context_object_name = 'compras'

# Vista para crear una compra
class CrearCompraView(CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'almacen/crear_compra.html'
    success_url = reverse_lazy('lista_compras')

# Vista para registrar merma
class RegistrarMermaView(CreateView):
    model = Merma
    form_class = MermaForm
    template_name = 'almacen/registrar_merma.html'
    
    def form_valid(self, form):
        merma = form.save()
        
        # Si la merma es de un insumo
        if merma.insumo:
            inventario = InventarioInsumo.objects.get(insumo=merma.insumo)
            inventario.cantidad -= merma.cantidad  # Restar la cantidad del inventario
            inventario.save()

        # Si la merma es de una galleta
        if merma.galleta:
            inventario = InventarioGalleta.objects.get(galleta=merma.galleta)
            inventario.cantidad -= merma.cantidad  # Restar la cantidad del inventario
            inventario.save()

        return redirect('lista_mermas')  # Redirigir a la lista de mermas

# Vista para listar mermas
class ListaMermasView(ListView):
    model = Merma
    template_name = 'almacen/lista_mermas.html'
    context_object_name = 'mermas'
