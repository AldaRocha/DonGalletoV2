from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from mermas_app.models import Merma
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
class ListaMermasView(PermissionRequiredMixin, TemplateView):
    permission_required = ["mermas_app.view_Merma"]
    login_url = "login"
    def handle_no_permission(self):
        return redirect("venta")
    template_name = "lista_mermas.html"
    def get_context_data(self):
        lista = Merma.objects.all()
        tipo_merma = self.request.GET.get("tipo_merma")
        fecha_registro = self.request.GET.get("fecha_registro")
        if tipo_merma:
            lista = lista.filter(tipo_merma=tipo_merma)
        if fecha_registro:
            try:
                fecha_obj = datetime.strptime(fecha_registro, "%Y-%m-%d").date()
                lista = lista.filter(fecha_registro__date=fecha_obj)
            except ValueError:
                pass
        return {
            "lista": lista
        }