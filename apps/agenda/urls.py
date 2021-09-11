from django.urls import path
from apps.agenda.views.gestionEventos.views import *
from apps.agenda.views.gestionTiposEventos.views import *
app_name = 'agenda'

urlpatterns = [
    # PAISES
    path('agenda/list/', DashboardAgenda.as_view(), name='dashboard'),
    path('agenda/updateEvento/<int:pk>/', UpdateEventosAgenda.as_view(), name='eventosUpdate'),
    path('agenda/deleteEvento/<int:pk>/', DeleteEventosAgenda.as_view(), name='eventosDelete'),
    path('agenda/tiposEventos/', TiposEventosListView.as_view(), name='tiposEventoList'),
    path('agenda/tiposEventos/add/', TiposEventosCreateView.as_view(), name='tiposEventoCreate'),
    path('agenda/tiposEventos/edit/<int:pk>/', TiposEventosEditView.as_view(), name='tiposEventoEdit'),
    path('agenda/tiposEventos/delete/<int:pk>/', TiposEventosDeleteView.as_view(), name='tiposEventoEdit'),
   # path('paises/add/', PaisesCreateView.as_view(), name='paises_create'),
   # path('paises/update/<int:pk>/', PaisesUpdateView.as_view(), name='paises_update'),
   # path('paises/delete/<int:pk>/', PaisesDeleteView.as_view(), name='paises_delete'),
]