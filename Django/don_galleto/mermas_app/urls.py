from django.urls import path
from mermas_app.views import ListaMermasView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lista_mermas/", login_required(ListaMermasView.as_view()), name="lista_mermas"),
]