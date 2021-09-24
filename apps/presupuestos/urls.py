from django.urls import path

from apps.presupuestos.views.presupuestos.views import *
from apps.presupuestos.views.presupuestosPlantilla.views import *

app_name = 'presupuestos'

urlpatterns = [
    # Presupuestos Base
    path('presupuestosPlantilla/list/', PresupuestosPlantillaListView.as_view(), name='presupuestosPlantilla_list'),
    path('presupuestosPlantilla/add/', PresupuestosPlantillaCreateView.as_view(), name='presupuestosPlantilla_create'),
    path('presupuestosPlantilla/update/<int:pk>/', PresupuestosPlantillaUpdateView.as_view(), name='presupuestosPlantilla_update'),
    path('presupuestosPlantilla/delete/<int:pk>/', PresupuestosPlantillaDeleteView.as_view(), name='presupuestosPlantilla_delete'),
    path('presupuestosPlantilla/pdf/<int:pk>/', PresupuestosPlantillaPdfView.as_view(), name='presupuestosPlantilla_pdf'),
    # Presupuestos
    path('presupuestos/list/', PresupuestosListView.as_view(), name='presupuestos_list'),
    path('presupuestos/add/', PresupuestosCreateView.as_view(), name='presupuestos_create'),
    path('presupuestos/update/<int:pk>/', PresupuestosUpdateView.as_view(), name='presupuestos_update'),
    path('presupuestos/delete/<int:pk>/', PresupuestosDeleteView.as_view(), name='presupuestos_delete'),
    path('presupuestos/pdf/<int:pk>/', PresupuestosPdfView.as_view(), name='presupuestos_pdf'),
]