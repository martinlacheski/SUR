from datetime import date, timedelta, datetime
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
        eventos = {}
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
            dia_hoy = date.today()
            hora_actual = datetime.today()
            rango = datetime.today() - timedelta(minutes=10)
            dias_aviso = diasAvisoEvento.objects.get(diasAntelacion__gte=0)

            # evento = eventosAgenda.objects.get(pk=8)
            # if evento.fechaNotificacion == dia_hoy:
            #     print("lpm")

            # Si hoy es dìa de notificación, empezamos. Sino, no hacemos nada
            if diaDeNotificacion(dia_hoy.weekday(), dias_aviso):
                tiposEventoSistema = tiposEvento.objects.filter(recordarSistema=True,
                                                                horarioRecordatorio__range=(rango.time(),
                                                                                            hora_actual.time()))
                data = eventosAgenda.objects.filter(tipoEvento__in=tiposEventoSistema)

                # Si no hay eventos en este rango horario, traigo los que ya se notificaron hoy
                if not data:
                    print("no encontramos datos, traemos los eventos de hoy ~")
                    eventos = eventosNotificadosHoy(eventosAgenda.objects.filter(ultimaNotificacionSist=dia_hoy))
                    return JsonResponse(eventos)

                # Si hay eventos, los analizo
                else:
                    # print("vamos al for")
                    for evento in data:
                        if evento.ultimaNotificacionSist == dia_hoy and (not evento.resuelto):
                            if evento.ultimaVistaNotifiSist == dia_hoy:
                                print("entro acá")
                                if evento.fechaNotificacion == dia_hoy:
                                    # Consultar si hay que seguir molestando al usuario o no
                                    eventos[evento.id] = ['notificar_heavy', str(evento.tipoEvento)]

                                else:
                                    eventos[evento.id] = ['no_notificar', str(evento.tipoEvento)]
                                # print("entra acá1")CC
                            else:
                                print("entro acá1")
                                if evento.fechaNotificacion == dia_hoy:
                                    eventos[evento.id] = ['notificar_heavy', str(evento.tipoEvento)]
                                else:
                                    eventos[evento.id] = ['no_notificar_pendiente', str(evento.tipoEvento)]
                                # print("entra acá2")
                        else:
                            if evento.vencido or evento.resuelto:
                                print("entro acá3")
                                # Mantenemos notificación de ev vencido el día de hoy
                                if evento.vencido and evento.fechaNotificacion == dia_hoy and (not evento.resuelto):
                                    eventos[evento.id] = ['no_notificar', str(evento.tipoEvento)]
                                    print("entro acá4")

                                print("el evento está vencido o el usuario ya lo descartó")
                                pass
                            else:
                                if evento.fechaNotificacion == dia_hoy:
                                    eventos[evento.id] = ['notificar_heavy', str(evento.tipoEvento)]
                                    print("mensaje a telgram")
                                    evento.vencido = True
                                    evento.ultimaNotificacionSist = date.today()
                                    evento.save()
                                elif evento.cantNotifSistema < dias_aviso.diasAntelacion:
                                    if restarDiasHabiles(evento.fechaNotificacion, dias_aviso.diasAntelacion) <= dia_hoy:
                                        eventos[evento.id] = ['notificar', str(evento.tipoEvento)]
                                        evento.ultimaNotificacionSist = date.today()
                                        evento.cantNotifSistema = evento.cantNotifSistema + 1
                                        evento.save()
                                        print("notificamos")
                                    else:
                                        print("re apurado. Todavía no hay que notificar che")
                                        pass
            else:
                print("no es dia de notificacion")
            print(eventos)
            return JsonResponse(eventos)


        # Marca que el user ya vió el evento y manda datos para mostrar su detalle
        if action == 'detail_evento':
            ev = eventosAgenda.objects.get(pk=request.POST['pk'])
            ev.ultimaVistaNotifiSist = date.today()
            ev.save()
            data_evento = datos_evento(request.POST['pk'])
            return JsonResponse(data_evento)

        # Marca qeu el evento ya fué cumplido. Los eventos cumplidos no son notificados nuevamente
        if action == 'evento_cumplido':
            data = {}
            ev = eventosAgenda.objects.get(pk=request.POST['pk'])
            ev.resuelto = True
            ev.save()
            return JsonResponse(data)




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