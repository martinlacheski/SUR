from django.urls import path
from apps.bot_telegram.views.notifIncidencias.views import *

app_name = 'bot'

urlpatterns = [
    path('usuarios/notifTo/list', notifIncidentesUsersListView.as_view(), name='notifIncidenList'),
    path('usuarios/notifTo/add', notifIncidentesUsersCreateView.as_view(), name='notifIncidenCreate'),
    path('usuarios/notifTo/edit/<int:pk>/', notifIncidentesUsersEditView.as_view(), name='notifIncidenEdit'),
    path('usuarios/notifTo/delete/<int:pk>/', notifIncidentesUsersDeleteView.as_view(), name='notifIncidenDelete'),
]