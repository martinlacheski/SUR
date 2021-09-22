import datetime
from datetime import timedelta
from apps.agenda.logicaNotificacion import *
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
            dia_hoy = datetime.date.today()
            dia_notif = diasAvisoEvento.objects.all()
            hora_actual = datetime.datetime.today()
            rango = datetime.datetime.today() - timedelta(minutes=10)
            eventos = {}


            evento_prueba = eventosAgenda.objects.get(pk=8)

            diasHabRestados = 0
            fechaNotifEvento = evento_prueba.fechaNotificacion
            fechaResultado = dia_hoy
            while diasHabRestados < dia_notif.diasAntelacion:
                fechaResultado = fechaNotifEvento - timedelta(days=1)
                if fechaResultado.weekday() in range(5):
                    diasHabRestados = diasHabRestados + 1




        """
            # Si hoy es dìa de notificación, empezamos. Sino, no hacemos nada
            if diaDeNotificacion(dia_hoy.weekday(), dia_notif[0]):
                tiposEventoSistema = tiposEvento.objects.filter(recordarSistema=True,
                                                                horarioRecordatorio__range=(rango.time(),
                                                                                            hora_actual.time()))
                data = eventosAgenda.objects.filter(tipoEvento__in=tiposEventoSistema)
                print(data)

                # Si no hay eventos en este rango horario, traigo los que ya se notificaron hoy
                if not data:
                    eventos = eventosNotificadosHoy(eventosAgenda.objects.filter(ultimaNotificacionSist=dia_hoy))
                    return JsonResponse(eventos)

                # Si hay eventos, los analizo
                else:
                    for evento in data:
                        if evento.ultimaNotificacionSist == dia_hoy:
                            eventos[evento.id] = 'no_notificar'
                        else:
                            if evento.vencido:
                                pass
                            else:
                                if evento.cantNotifSistema >= dia_notif.diasAntelacion:
                                    eventos[evento.id] = 'notificar_heavy'
                                    print("mensaje a telgram")
                                    evento_instancia = eventosAgenda.objects.get(pk=evento.id)
                                    evento_instancia.vencido = True
                                    evento_instancia.save()
                                if evento.cantNotifSistema < dia_notif.diasAntelacion:
                                    if evento.ultimaNotificacionSist == dia_hoy:
                                        eventos[evento.id] = 'no_notificar'
                                    else:


                print(eventos)
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
    data['fechaNotif'] = str(evento.fechaNotificacion.day) + \
                         "/"+ str(evento.fechaNotificacion.month) + \
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