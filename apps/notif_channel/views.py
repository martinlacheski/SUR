from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView
from apps.notif_channel.models import notificacionesGenerales
from apps.usuarios.models import Usuarios
import datetime

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
            n = notificacionesGenerales.objects.order_by('-fechaNotificacion').exclude(estado='resuelta').reverse()[:10]
            for i in n:
                data.append(i.toJSON())
            return JsonResponse(data, safe=False)

        if action == 'detalle_notif':
            user = Usuarios.objects.get(pk=request.POST['user'])
            print("id de notif que viene desde fron end: " + request.POST['pk'])
            n = notificacionesGenerales.objects.get(pk=request.POST['pk'])
            data.append(n.toJSON())
            n.estado = 'vista'
            n.fechaRevisionUser = datetime.datetime.today()
            n.save()
            return JsonResponse (data, safe=False)