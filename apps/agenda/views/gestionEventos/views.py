from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from apps.agenda.models import *
from apps.agenda.forms import *
from apps.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse


class DashboardAgenda(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    template_name = 'gestionEventos/list.html'
    model = eventosAgenda
    form_class = GestionEventosForm
    permission_required = 'agenda.add_tiposEventos'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
            #data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administración'
        return context



