from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.mixins import ValidatePermissionRequiredMixin


class ExampleView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'gestionEventos/list.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administración'
        return context



