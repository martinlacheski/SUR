import datetime
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from apps.agenda.models import *
from apps.agenda.forms import *
from apps.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from apps.agenda.jobs import scheduler_eventos


class DashboardAgenda(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    template_name = 'gestionEventos/list.html'
    model = eventosAgenda
    form_class = GestionEventosForm
    permission_required = 'agenda.add_eventosagenda'
    success_url = reverse_lazy('agenda:dashboard')



    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        if action == 'add':
            try:
                form = self.get_form()
                if form.is_valid():
                    form.save()
                    # scheduler_eventos()
                else:
                    print(form.errors)
            except Exception as e:
                print(str(e))
            return HttpResponseRedirect(self.success_url)

        # Busca datos de un evento en específico para modal en calendar
        if action == 'search_data':
            data = datos_evento(request.POST['pk'])
            return JsonResponse(data)

        # Vendrá en ppróxima versión. Que avise al sistema. Se requiere integración con OTRA lib
        """
        if action == 'get_news':

            # Obtenemos eventos que se muesten en Sistema y su horario de notif sea
            # cercano al actual (margen de 10 min)
            hora_actual = datetime.datetime.today()
            rango = datetime.datetime.today() - timedelta(minutes=10)
            tiposEventoSistema = tiposEvento.objects.filter(recordarSistema=True,
                                                            horarioRecordatorio__range=(rango.time(), hora_actual.time()))
            data = eventosAgenda.objects.filter(tipoEvento__in=tiposEventoSistema).values('id')

            # Comprobamos tipo de repeticion de evento

            for evento in data:
                if(evento.repeticion == ''):
                    eventos_display.a

            eventoSist = [evento for evento in data]
            data = tuple(eventoSist)
            # preguntar si es único (si lo es, verificar que sea fecha de hoy y enviar)
            # preguntar si es diario(si lo es, enviar)
            # preguntar si es semanal (si su dia de la semana es el día de la semana actual, enviar)
            # preguntar si es mensual (primero verificar si su día es el último dia del mes y el día del mes actual lo es, enviar)
            #                         (luego si su día del mes es el día del mes actual, tambien enviar)
            return JsonResponse(data, safe=False)
        """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eventos'] = eventosAgenda.objects.all()
        context['update_url'] = 'agenda/updateEvento/'
        context['delete_url'] = '/agenda/deleteEvento/'
        context['dashboard_url'] = reverse_lazy('agenda:dashboard')
        context['action'] = 'add'
        return context


class UpdateEventosAgenda(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = eventosAgenda
    form_class = GestionEventosForm
    success_url = reverse_lazy('agenda:dashboard')
    permission_required = 'agenda.change_eventosagenda'
    template_name = 'gestionEventos/list.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        if action == 'edit':
            try:
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    print(form.errors)
            except Exception as e:
                print(str(e))
            return HttpResponseRedirect(self.success_url)
        if action == 'search_data':
            data = datos_evento(request.POST['pk'])
            return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eventos'] = eventosAgenda.objects.all()
        context['update_url'] = 'agenda/updateEvento/'
        context['action'] = 'edit'
        context['delete_url'] = '/agenda/deleteEvento/'
        return context

class DeleteEventosAgenda(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = eventosAgenda
    success_url = reverse_lazy('agenda:dashboard')
    permission_required = 'agenda.delete_eventosagenda'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        id = request.POST['pk']
        action = request.POST['action']
        if action == 'delete':
            data = {}
            try:
                self.object.delete()
                data['redirect'] = self.url_redirect
                data['check'] = 'ok'
            except Exception as e:
                data['check'] = str(e)
        return JsonResponse(data)


def datos_evento(evento_id):
    data = {}
    evento = eventosAgenda.objects.get(pk=evento_id)
    data['tipoEvento'] = str(evento.tipoEvento)
    data['fechaNotif'] = str(evento.fechaNotificacion.day) +\
                             "/"+ str(evento.fechaNotificacion.month) +\
                             "/" + str(evento.fechaNotificacion.year)
    data['descripcion'] = str(evento.descripcion)
    data['repeticion'] = str(evento.repeticion)
    data['userAsoc'] = str(evento.tipoEvento.usuarioNotif)
    data['notifMediante'] = (['Email', evento.tipoEvento.recordarEmail],
                             ['Sistema', evento.tipoEvento.recordarSistema],
                             ['Telegram', evento.tipoEvento.recordarTelegram])
    return data