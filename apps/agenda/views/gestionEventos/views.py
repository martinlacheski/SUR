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
        notificaciones = {}
        if action == 'add':
            try:
                form = self.get_form()
                if form.is_valid():
                    print(form.cleaned_data['fechaFinalizacion'])
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

        # Obtenemos eventos que se muesten en Sistema y su horario de notif sea cercano al actual (margen de 10 min)
        if action == 'get_news':
            hora_actual = datetime.datetime.today()
            rango = datetime.datetime.today() - timedelta(minutes=10)
            print(hora_actual)
            print(rango)

            tiposEventoSistema = tiposEvento.objects.filter(recordarSistema=True,
                                                            horarioRecordatorio__range=(rango.time(), hora_actual.time()))
            print(tiposEventoSistema)
            data = eventosAgenda.objects.filter(tipoEvento__in=tiposEventoSistema)
            print(data)

            return JsonResponse(data)

        #   acá iría un if action 'news_readed' o algo asi y aceptaría un array de notificaciones

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
    data['fechaFinal'] = str(evento.fechaNotificacion.day) + \
                         "/" + str(evento.fechaNotificacion.month) + \
                         "/" + str(evento.fechaNotificacion.year)
    data['descripcion'] = str(evento.descripcion)
    data['repeticion'] = str(evento.repeticion)
    data['userAsoc'] = str(evento.tipoEvento.usuarioNotif)
    data['notifMediante'] = (['Sistema', evento.tipoEvento.recordarSistema],
                             ['Telegram', evento.tipoEvento.recordarTelegram])
    return data

def save_ultima_notif(idevento):
    event = eventosAgenda.objects.get(pk=idevento)
    event.ultimaNotificacionSist = datetime.date.today()
    event.save()

def save_ultima_vista(idevento):
    event = eventosAgenda.objects.get(pk=idevento)
    event.ultimaVistaNotifiSist = datetime.date.today()
    event.save()