from django.urls import path
from medidas_app.views import ListaMedidasView, CrearMedidasView, EditarMedidasView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_medidas/", login_required(ListaMedidasView.as_view()), name="lista_medidas"),
    path("crear_medidas/", login_required(CrearMedidasView.as_view()), name="crear_medidas"),
    path("editar_medidas/<int:id>", login_required(EditarMedidasView.as_view()), name="editar_medidas")
]