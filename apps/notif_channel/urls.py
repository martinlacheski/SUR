# chat/urls.py
from django.urls import path

from apps.notif_channel.views import NotificacionesNotifView

#Las URL se van a llamar dentro del body. No importa cual tenga.
# es mas. Probablemente no se use este urls.py
urlpatterns = [
    path('notificaciones/updateList/', NotificacionesNotifView.as_view(), name='listNotificaciones'),
]