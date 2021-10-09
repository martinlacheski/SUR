from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView

from apps.agenda.forms import GestionNotifEventosForm
from apps.agenda.models import diasAvisoEvento
from apps.mixins import ValidatePermissionRequiredMixin

class NotificacionesCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = diasAvisoEvento
    form_class = GestionNotifEventosForm
    template_name = 'gestionNotificaciones/create.html'
    permission_required = 'agenda.change_diasavisoevento'
    success_url = reverse_lazy('agenda:notifEventosList')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            data['redirect'] = self.url_redirect
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un esquema de Notificaciones'
        context['entity'] = 'Notificaiones'
        context['create_url'] = reverse_lazy('agenda:notifEventosCreate')
        context['list_url'] = reverse_lazy('agenda:notifEventosList')
        context['action'] = 'add'
        return context


class NotificacionesEditView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = diasAvisoEvento
    form_class = GestionNotifEventosForm
    template_name = 'gestionNotificaciones/create.html'
    permission_required = 'agenda.change_diasavisoevento'
    success_url = reverse_lazy('agenda:notifEventosList')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            form.save()
            data['redirect'] = self.success_url
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Configurar Notificaciones'
        context['entity'] = 'Notificaciones'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('agenda:notifEventosList')
        return context


class NotificacionesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = diasAvisoEvento
    template_name = 'gestionNotificaciones/list.html'
    permission_required = 'agenda.view_diasavisoevento'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in diasAvisoEvento.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Configurar Notificaciones'
        context['entity'] = 'Notificaciones'
        context['action'] = 'list'
        context['create_url'] = reverse_lazy('agenda:notifEventosCreate')
        context['notifCreada'] = notif_creada()
        return context


def notif_creada():
    notificaciones = diasAvisoEvento.objects.all()
    if notificaciones:
        return 'verdadero'
    else:
        return 'falso'
