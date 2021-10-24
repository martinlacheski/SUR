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
from apps.agenda import jobs


class DashboardAgenda(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    template_name = 'gestionEventos/list.html'
    model = eventosAgenda
    form_class = GestionEventosForm
    permission_required = 'agenda.add_eventosagenda'
    success_url = reverse_lazy('agenda:dashboard')

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        if action == 'add':
            try:
                form = self.get_form()
                if form.is_valid():
                    data = form.save()
                    jobs.scheduler_evento(data['eventoObj'])
                else:
                    print(form.errors)
            except Exception as e:
                print(str(e))
            return HttpResponseRedirect(self.success_url)

        # Busca datos de un evento en específico para modal en calendar
        if action == 'search_data':
            data = datos_evento_evID(request.POST['pk'])
            return JsonResponse(data)


        # TO-DO Se tiene que refactorizar para que unicamente toque la tabla eventosAgenda
        if action == 'evento_cumplido':
            print("refactorizame")
            # data = {}
            # notif = notificaciones.objects.get(pk=request.POST['pk'])
            # user = Usuarios.objects.get(pk=request.POST['user'])
            # ev = eventosAgenda.objects.get(pk=notif.eventoAsoc.id)
            # self.descartarNotificaciones(notif.eventoAsoc, user)
            # ev.resuelto = True
            # ev.save()
            # return JsonResponse(data)

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
                    data = form.save()
                    # TO-DO acá va la ¿modificacion? de un job para que luego notifique al cliente
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
                evento = eventosAgenda.objects.get(pk=self.object.id)
                self.object.estado = False
                self.object.save()
                data['redirect'] = self.url_redirect
                data['check'] = 'ok'
            except Exception as e:
                data['check'] = str(e)
        return JsonResponse(data)

def datos_evento_evID(ev_id):
    data = {}
    U = ""
    evento = eventosAgenda.objects.get(pk=ev_id)
    data['tipoEvento'] = str(evento.tipoEvento)
    data['fechaNotif'] = str(evento.fechaNotificacion.day) + \
                         "/" + str(evento.fechaNotificacion.month) + \
                         "/" + str(evento.fechaNotificacion.year)
    usuariosAsoc = notificacionUsuarios.objects.filter(tipoEvento=evento.tipoEvento)
    for user in usuariosAsoc:
        U = U + str(user.usuarioNotif.username) + ', '
    data['usuariosAsoc'] = U
    if evento.fechaFinalizacion:
        data['fechaFinal'] = str(evento.fechaFinalizacion.day) + \
                              "/" + str(evento.fechaFinalizacion.month) + \
                              "/" + str(evento.fechaFinalizacion.year)
    if evento.repeticion:
        data['repeticion'] = str(evento.repeticion)
    data['descripcion'] = str(evento.descripcion)
    data['notifMediante'] = (['Sistema', evento.tipoEvento.recordarSistema],
                             ['Telegram', evento.tipoEvento.recordarTelegram])
    return data


