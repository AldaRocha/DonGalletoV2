from django.views.generic.base import TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth import login
from don_galleto.forms import RegistroForm

class home(TemplateView):
    template_name = "home.html"
    def get_context_data(self):
        return {}

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