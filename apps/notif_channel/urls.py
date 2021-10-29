# chat/urls.py
from django.urls import path

from apps.notif_channel.views import NotificacionesNotifView, NotificacionesListView


app_name = 'notificaciones'
urlpatterns = [
    path('notificaciones/updateList/', NotificacionesNotifView.as_view(), name='listNotificaciones'),
    path('notificaciones/list/', NotificacionesListView.as_view(), name='listNotificacionesCompleta'),
]