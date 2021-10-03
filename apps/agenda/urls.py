from django.urls import path
from apps.agenda.views.gestionEventos.views import *
from apps.agenda.views.gestionTiposEventos.views import *
from apps.agenda.views.gestionNotificaciones.views import *
app_name = 'agenda'

urlpatterns = [
    path('agenda/list/', DashboardAgenda.as_view(), name='dashboard'),
    path('agenda/updateEvento/<int:pk>/', UpdateEventosAgenda.as_view(), name='eventosUpdate'),
    path('agenda/deleteEvento/<int:pk>/', DeleteEventosAgenda.as_view(), name='eventosDelete'),

    path('agenda/tiposEventos/', TiposEventosListView.as_view(), name='tiposEventoList'),
    path('agenda/tiposEventos/add/', TiposEventosCreateView.as_view(), name='tiposEventoCreate'),
    path('agenda/tiposEventos/edit/<int:pk>/', TiposEventosEditView.as_view(), name='tiposEventoEdit'),
    path('agenda/tiposEventos/delete/<int:pk>/', TiposEventosDeleteView.as_view(), name='tiposEventoDelete'),

    path('agenda/gestionNotif/', NotificacionesListView.as_view(), name='notifEventosList'),
    path('agenda/gestionNotif/edit/<int:pk>/', NotificacionesEditView.as_view(), name='notifEventosEdit'),
    path('agenda/gestionNotif/add/', NotificacionesCreateView.as_view(), name='notifEventosCreate'),
]