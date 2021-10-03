from datetime import date, timedelta, datetime

import apps.agenda.models
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
        # data = {}
        # eventos = {}
        # notificaciones = {}
        if action == 'add':
            dias_aviso_add = diasAvisoEvento.objects.get(diasAntelacion__gte=0)
            dia_hoy_add = date.today()
            try:
                form = self.get_form()
                if form.is_valid():
                    # al guardarse, evaluamos si se deben crear notificaciones o no
                    data = form.save()
                    if restarDiasHabiles(data['eventoObj'].fechaNotificacion, dias_aviso_add.diasAntelacion) <= dia_hoy_add:
                        self.crearNotificaciones(data['eventoObj'])
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
        # if action == 'get_news':
        #     dia_hoy = date.today()
        #     hora_actual = datetime.today()
        #     rango = datetime.today() - timedelta(minutes=10)
        #     dias_aviso = diasAvisoEvento.objects.get(diasAntelacion__gte=0)
        #
        #     # evento = eventosAgenda.objects.get(pk=8)
        #     # if evento.fechaNotificacion == dia_hoy:
        #     #     print("lpm")
        #
        #     # Si hoy es dìa de notificación, empezamos. Sino, no hacemos nada
        #     if diaDeNotificacion(dia_hoy.weekday(), dias_aviso):
        #         tiposEventoSistema = tiposEvento.objects.filter(recordarSistema=True,
        #                                                         horarioRecordatorio__range=(rango.time(),
        #                                                                                     hora_actual.time()))
        #         data = eventosAgenda.objects.filter(tipoEvento__in=tiposEventoSistema)
        #
        #         # Si no hay eventos en este rango horario, traigo los que ya se notificaron hoy
        #         if not data:
        #             print("no encontramos datos, traemos los eventos de hoy ~")
        #             eventos = eventosNotificadosHoy(eventosAgenda.objects.filter(ultimaNotificacionSist=dia_hoy))
        #             return JsonResponse(eventos)
        #
        #         # Si hay eventos, los analizo
        #         else:
        #             # print("vamos al for")
        #             for evento in data:
        #                 if evento.ultimaNotificacionSist == dia_hoy and (not evento.resuelto):
        #                     if evento.ultimaVistaNotifiSist == dia_hoy:
        #                         print("entro acá")
        #                         if evento.fechaNotificacion == dia_hoy:
        #                             # Consultar si hay que seguir molestando al usuario o no
        #                             eventos[evento.id] = ['notificar_heavy', str(evento.tipoEvento)]
        #
        #                         else:
        #                             eventos[evento.id] = ['no_notificar', str(evento.tipoEvento)]
        #                         # print("entra acá1")CC
        #                     else:
        #                         print("entro acá1")
        #                         if evento.fechaNotificacion == dia_hoy:
        #                             eventos[evento.id] = ['notificar_heavy', str(evento.tipoEvento)]
        #                         else:
        #                             eventos[evento.id] = ['no_notificar_pendiente', str(evento.tipoEvento)]
        #                         # print("entra acá2")
        #                 else:
        #                     if evento.vencido or evento.resuelto:
        #                         print("entro acá3")
        #                         # Mantenemos notificación de ev vencido el día de hoy
        #                         if evento.vencido and evento.fechaNotificacion == dia_hoy and (not evento.resuelto):
        #                             eventos[evento.id] = ['no_notificar', str(evento.tipoEvento)]
        #                             print("entro acá4")
        #
        #                         print("el evento está vencido o el usuario ya lo descartó")
        #                         pass
        #                     else:
        #                         if evento.fechaNotificacion == dia_hoy:
        #                             eventos[evento.id] = ['notificar_heavy', str(evento.tipoEvento)]
        #                             print("mensaje a telgram")
        #                             evento.vencido = True
        #                             evento.ultimaNotificacionSist = date.today()
        #                             evento.save()
        #                         elif evento.cantNotifSistema < dias_aviso.diasAntelacion:
        #                             if restarDiasHabiles(evento.fechaNotificacion,
        #                                                  dias_aviso.diasAntelacion) <= dia_hoy:
        #                                 eventos[evento.id] = ['notificar', str(evento.tipoEvento)]
        #                                 evento.ultimaNotificacionSist = date.today()
        #                                 evento.cantNotifSistema = evento.cantNotifSistema + 1
        #                                 evento.save()
        #                                 print("notificamos")
        #                             else:
        #                                 print("re apurado. Todavía no hay que notificar che")
        #                                 pass
        #     else:
        #         print("no es dia de notificacion")
        #     print(eventos)
        #     return JsonResponse(eventos)

        # Marca que el user ya vió el evento y manda datos para mostrar su detalle  # action descar

        if action == 'detail_evento':
            # ev = eventosAgenda.objects.get(pk=request.POST['pk'])
            # ev.ultimaVistaNotifiSist = date.today()
            # ev.save()

            notifs_evento = notificaciones.objects.filter(eventoAsoc=request.POST['pk'],
                                                          usuarioNotif=request.POST['user'])
            for n in notifs_evento:
                n.ultVistaUserSist = date.today()
                n.save()
            print(request.POST['pk'])
            data_evento = datos_evento(request.POST['pk'])
            return JsonResponse(data_evento)

        # Marca qeu el evento ya fué resuelto. Los eventos resueltos no generan notificaciones
        if action == 'evento_cumplido':
            data = {}
            ev = eventosAgenda.objects.get(pk=request.POST['pk'])
            ev.resuelto = True
            ev.save()
            return JsonResponse(data)

        # action de prueba. Luego será borrado porque se va a ejcutar con un cron
        # Representa al algoritmo que se ejecuta una vez por día
        if action == 'prueba':
            data = {}
            dia_hoy = date.today()
            dias_aviso = diasAvisoEvento.objects.get(diasAntelacion__gte=0)

            #   Si es dia de notificacion traemos todos los eventos NO resueltos y todas las notificaciones
            if diaDeNotificacion(dia_hoy.weekday(), dias_aviso):
                print("Es día de notificacion")
                eventos = eventosAgenda.objects.filter(resuelto=False, estado=True)
                print("encontramos estos eventos: " + str(eventos))
                # Por cada evento, vemos si éste está reflejado en una notificación
                for evento in eventos:
                    # Si el evento no tiene asociación en tabla notificaciones, analizamos si la creamos
                    if not apps.agenda.models.notificaciones.objects.filter(eventoAsoc=evento):
                        print("no encontro notif asociada a evento, vamos a crear una")
                        #   En caso de que la resta de días hábiles de que el resultado es menor o igual
                        #   a la fecha de hoy, agregamos una notificación POR CADA USUARIO asignado al tipo de evento
                        if restarDiasHabiles(evento.fechaNotificacion, dias_aviso.diasAntelacion) <= dia_hoy:
                            print("la resta dió que creamos notificaciones")
                            self.crearNotificaciones(evento)
                            print("Ya está. Creamos las notif")
                    # Si el evento SI tiene una notificación asociada, la analizamos
                    else:
                        print("el evento tenía notifs asociadas. Las analizamos")
                        # Si el evento está vencido, entonces descartamos sus notificaciones
                        if evento.vencido:
                            print("el evento está vencido")
                            for n in apps.agenda.models.notificaciones.objects.filter(eventoAsoc=evento):
                                n.notificacion = 'no'
                                n.save()
                            print("descartamos todas sus notificaciones")
                        else:
                            print("el evento no está vencido")
                            # Si el evento vence hoy, entonces sus notificaciones son urgentes
                            if evento.fechaNotificacion == dia_hoy:
                                evento.vencido = True
                                print("la fecha de notif era hoy, ahora el evento está vencido")
                                for n in apps.agenda.models.notificaciones.objects.filter(eventoAsoc=evento):
                                    n.notificacion = 'urgent'
                                    n.save()
                                print("todas sus notificaciones son urgentes")
                                evento.save()
                            else:
                                print("el evento no se notifica hoy, vamos a evaluar si debemos agreagar una nueva noti")
                                #   Si la resta de días hábiles a la fecha de notificación es menor que la fecha actual,
                                #   agregamos otra notificación a la tabla de notificaciones
                                fecha_result = restarDiasHabiles(evento.fechaNotificacion, dias_aviso.diasAntelacion)
                                if dia_hoy >= fecha_result and dia_hoy < evento.fechaNotificacion:
                                    print("agregamos nuevas notif por usuario")
                                    self.crearNotificaciones(evento)
                                else:
                                    print("no agregamos nuevas notif")
            else:
                print("no es día de notificación")

            return JsonResponse(data)

        # este action no va a ser borrado porque consultará la tabla notificaciones cada tanto
        if action == 'prueba2':
            data = {}
            dia_hoy = date.today()
            hora_actual = datetime.today()
            rango = datetime.today() - timedelta(minutes=10)
            dias_aviso = diasAvisoEvento.objects.get(diasAntelacion__gte=0)

            #   Si es dia de notificacion traemos todos los eventos y todas las notificaciones
            if diaDeNotificacion(dia_hoy.weekday(), dias_aviso):
                print("hoy es dia de notificacion")
                # Buscamos las notificaciones asociadas al usuario que está actualmente logueado
                # y que no estén resueltas
                notifs = apps.agenda.models.notificaciones.objects.filter(usuarioNotif=request.POST['user'])
                notifs = notifs.filter(resueltaPorUserSist__isnull=True)

                for n in notifs:
                    if n.notificacion == 'yes':
                        print("vamos a notificar")
                        if n.ultNotifSist == dia_hoy:
                            print("la ultima notificación fué el día de hoy")
                            if n.ultVistaUserSist == dia_hoy:
                                print("la ultima vista de esa notif fué hoy")
                                n.notificacion = 'passive'
                                data[n.id] = ['no_notificar', str(n.eventoAsoc.tipoEvento)]
                            else:
                                print("aún no vieron la notif")
                                n.notificacion = 'pending'
                                data[n.id] = ['no_notificar_pendiente', str(n.eventoAsoc.tipoEvento)]
                        else:
                            print("aún no se ha notificado la notif el día de hoy")
                            print(hora_actual.time())
                            print(n.eventoAsoc.tipoEvento.horarioRecordatorio)
                            print(rango.time())
                            if rango.time() <= n.eventoAsoc.tipoEvento.horarioRecordatorio <= hora_actual.time():
                                print("estamos en rango horario y notificamos")
                                data[n.id] = ['notificar', str(n.eventoAsoc.tipoEvento)]
                                n.ultNotifSist = dia_hoy
                                n.cantNotifSist = n.cantNotifSist + 1
                                n.save()
                            else:
                                print("no estamos en horario de notificacion")

                    elif n.notificacion == 'no':
                        print("no notificamos esta")
                        pass
                    elif n.notificacion == 'pending':
                        print("hay una notificacion pendiente")
                        data[n.id] = ['no_notificar_pendiente', str(n.eventoAsoc.tipoEvento)]
                    elif n.notificacion == 'passive':
                        print("notifiacion pasiva")
                        data[n.id] = ['no_notificar', str(n.eventoAsoc.tipoEvento)]
                    elif n.notificacion == 'urgent':
                        data[n.id] = ['notificar_heavy', str(n.eventoAsoc.tipoEvento)]
                        print("notificacion urgente")
                        print("enviar msj telegram a user")

            else:
                print("hoy no es día de notificacion")
            print(data)
            return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eventos'] = eventosAgenda.objects.all()
        context['update_url'] = 'agenda/updateEvento/'
        context['delete_url'] = '/agenda/deleteEvento/'
        context['dashboard_url'] = reverse_lazy('agenda:dashboard')
        context['action'] = 'add'
        return context

    def crearNotificaciones(self, EV):
        for user in notificacionUsuarios.objects.filter(tipoEvento=EV.tipoEvento):
            newNotif = apps.agenda.models.notificaciones()
            newNotif.notificarSist = EV.tipoEvento.recordarSistema
            newNotif.notificarTel = EV.tipoEvento.recordarTelegram
            newNotif.notificacion = 'yes'
            newNotif.eventoAsoc = EV
            newNotif.usuarioNotif = user.usuarioNotif
            newNotif.save()


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
            dias_aviso_edit = diasAvisoEvento.objects.get(diasAntelacion__gte=0)
            dia_hoy_edit = date.today()
            try:
                form = self.get_form()
                if form.is_valid():
                    data = form.save()
                    # Descartamos notificaciones viejas
                    print("descartamos notificaciones viejas por las dudas")
                    self.descartarNotificaciones(data['eventoObj'])

                    # Añadimos nuevas notificaciones en caso de cumplir la condición
                    if restarDiasHabiles(data['eventoObj'].fechaNotificacion, dias_aviso_edit.diasAntelacion) <= dia_hoy_edit:
                        print("agregamos notificaciones para el evento modificado")
                        self.crearNotificaciones(data['eventoObj'])
                    else:
                        print("no se tenian que agregar notif para el evento aún")
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

    def crearNotificaciones(self, EV):
        for user in notificacionUsuarios.objects.filter(tipoEvento=EV.tipoEvento):
            newNotif = apps.agenda.models.notificaciones()
            newNotif.notificarSist = EV.tipoEvento.recordarSistema
            newNotif.notificarTel = EV.tipoEvento.recordarTelegram
            newNotif.notificacion = 'yes'
            newNotif.eventoAsoc = EV
            newNotif.usuarioNotif = user.usuarioNotif
            newNotif.save()

    def descartarNotificaciones(self, EV):
        notif = notificaciones.objects.filter(eventoAsoc=EV.id)
        if notif:
            for n in notif:
                n.notificacion = 'no'
                n.save()



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
                evento = eventosAgenda.objects.get(pk=self.object.id)
                # descartamos notificaciones de ese evento
                if evento:
                    self.descartarNotificaciones(evento)

                # Damos de baja el evento
                self.object.estado = False
                self.object.save()
                data['redirect'] = self.url_redirect
                data['check'] = 'ok'
            except Exception as e:
                data['check'] = str(e)
        return JsonResponse(data)

    def descartarNotificaciones(self, EV):
        notif = notificaciones.objects.filter(eventoAsoc=EV.id)
        if notif:
            for n in notif:
                n.notificacion = 'no'
                n.save()


def datos_evento(notif_id):
    data = {}
    notif = notificaciones.objects.get(pk=notif_id)
    evento_id = notif.eventoAsoc.id
    print(evento_id)
    evento = eventosAgenda.objects.get(pk=evento_id)
    data['tipoEvento'] = str(evento.tipoEvento)
    data['fechaNotif'] = str(evento.fechaNotificacion.day) + \
                         "/" + str(evento.fechaNotificacion.month) + \
                         "/" + str(evento.fechaNotificacion.year)
    # data['fechaFinal'] = str(evento.fechaNotificacion.day) + \
    #                      "/" + str(evento.fechaNotificacion.month) + \
    #                      "/" + str(evento.fechaNotificacion.year)
    data['descripcion'] = str(evento.descripcion)
    # data['repeticion'] = str(evento.repeticion)
    data['notifMediante'] = (['Sistema', evento.tipoEvento.recordarSistema],
                             ['Telegram', evento.tipoEvento.recordarTelegram])
    return data



