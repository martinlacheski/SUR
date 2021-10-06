from django.urls import path

from apps.trabajos.views.planificaciones.views import *
from apps.trabajos.views.trabajos.views import *

app_name = 'trabajos'

urlpatterns = [
    # Trabajos
    path('trabajos/list/', TrabajosListView.as_view(), name='trabajos_list'),
    path('trabajos/add/', TrabajosCreateView.as_view(), name='trabajos_create'),
    path('trabajos/express/', TrabajosExpressCreateView.as_view(), name='trabajos_create_express'),
    path('trabajos/update/<int:pk>/', TrabajosUpdateView.as_view(), name='trabajos_update'),
    path('trabajos/confirm/<int:pk>/', TrabajosConfirmView.as_view(), name='trabajos_confirm'),
    path('trabajos/deliver/<int:pk>/', TrabajosDeliverView.as_view(), name='trabajos_deliver'),
    path('trabajos/delete/<int:pk>/', TrabajosDeleteView.as_view(), name='trabajos_delete'),
    path('trabajos/pdf/<int:pk>/', TrabajosPdfView.as_view(), name='trabajos_pdf'),
    # Planificacion de Trabajos
    path('planificaciones/list/', PlanificacionesSemanalesListView.as_view(), name='planificaciones_list'),
    path('planificaciones/add/', PlanificacionesSemanalesCreateView.as_view(), name='planificaciones_create'),
    path('planificaciones/update/<int:pk>/', PlanificacionesSemanalesUpdateView.as_view(), name='planificaciones_update'),
    path('planificaciones/delete/<int:pk>/', PlanificacionesSemanalesDeleteView.as_view(), name='planificaciones_delete'),
    path('planificaciones/pdf/<int:pk>/', PlanificacionesSemanalesPdfView.as_view(), name='planificaciones_pdf'),
]