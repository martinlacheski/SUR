from django.urls import path
from apps.agenda.views.gestionEventos.views import *
app_name = 'agenda'

urlpatterns = [
    # PAISES
    path('agenda/list/', ExampleView.as_view(), name='dashboard'),
   # path('paises/add/', PaisesCreateView.as_view(), name='paises_create'),
   # path('paises/update/<int:pk>/', PaisesUpdateView.as_view(), name='paises_update'),
   # path('paises/delete/<int:pk>/', PaisesDeleteView.as_view(), name='paises_delete'),
]