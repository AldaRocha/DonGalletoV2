from django.views.generic.base import TemplateView

class home(TemplateView):
    template_name = "home.html"
    def get_context_data(self):
        return {}