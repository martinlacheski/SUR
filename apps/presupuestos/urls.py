from django.urls import path

from apps.presupuestos.views.presupuestos.views import *
from apps.presupuestos.views.presupuestosBase.views import *

app_name = 'presupuestos'

urlpatterns = [
    # Presupuestos Base
    path('presupuestosBase/list/', PresupuestosBaseListView.as_view(), name='presupuestosBase_list'),
    path('presupuestosBase/add/', PresupuestosBaseCreateView.as_view(), name='presupuestosBase_create'),
    path('presupuestosBase/update/<int:pk>/', PresupuestosBaseUpdateView.as_view(), name='presupuestosBase_update'),
    path('presupuestosBase/delete/<int:pk>/', PresupuestosBaseDeleteView.as_view(), name='presupuestosBase_delete'),
    path('presupuestosBase/pdf/<int:pk>/', PresupuestosBasePdfView.as_view(), name='presupuestosBase_pdf'),
    # Presupuestos
    path('presupuestos/list/', PresupuestosListView.as_view(), name='presupuestos_list'),
    path('presupuestos/add/', PresupuestosCreateView.as_view(), name='presupuestos_create'),
    path('presupuestos/update/<int:pk>/', PresupuestosUpdateView.as_view(), name='presupuestos_update'),
    path('presupuestos/delete/<int:pk>/', PresupuestosDeleteView.as_view(), name='presupuestos_delete'),
    path('presupuestos/pdf/<int:pk>/', PresupuestosPdfView.as_view(), name='presupuestos_pdf'),
]