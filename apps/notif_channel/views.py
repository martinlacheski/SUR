from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView
from apps.notif_channel.models import notificacionesGenerales
from apps.usuarios.models import Usuarios
import datetime
from django.urls import reverse_lazy


from apps.mixins import ValidatePermissionRequiredMixin

class NotificacionesNotifView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'notif_channel.view_notificacionesgenerales'
    model = notificacionesGenerales

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        action = request.POST['action']
        data = []
        if action == 'update_notifs':
            notifs = {}
            n = notificacionesGenerales.objects.order_by('-pk').exclude(estado='resuelta')[:10]
            for i in reversed(n):
                data.append(i.toJSON())
            return JsonResponse(data, safe=False)

        if action == 'detalle_notif':
            n = notificacionesGenerales.objects.get(pk=request.POST['pk'])
            data.append(n.toJSON())
            if not n.fechaRevisionUser:
                n.estado = 'vista'
                n.fechaRevisionUser = datetime.datetime.today()
                n.save()
            return JsonResponse (data, safe=False)

class NotificacionesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'notif_channel.view_notificacionesgenerales'
    model = notificacionesGenerales
    template_name = 'completoNotificaciones/list.html'
    success_url = reverse_lazy('notificaciones:listNotificacionesCompleta')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        action = request.POST['action']
        data = []

        if action == 'search_data':
            notifs = {}
            n = notificacionesGenerales.objects.order_by('-pk')
            for i in n:
                data.append(i.toJSON())
            return JsonResponse(data, safe=False)

        if action == 'detalle_notif_completo':
            n = notificacionesGenerales.objects.get(pk=request.POST['pk'])
            data.append(n.toJSON())
            if not n.fechaRevisionUser:
                n.estado = 'vista'
                n.fechaRevisionUser = datetime.datetime.today()
                n.save()
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notifi_list_url'] = self.success_url
        context['title'] = 'Histórico de Notificaciones'
        context['entity'] = 'Notificaciones'
        return context
