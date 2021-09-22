from django.urls import path

from apps.presupuestos.views.presupuestosBase.views import *

app_name = 'presupuestos'

urlpatterns = [
    # Presupuestos Base
    path('presupuestosBase/list/', PresupuestosBaseListView.as_view(), name='presupuestosBase_list'),
    path('presupuestosBase/add/', PresupuestosBaseCreateView.as_view(), name='presupuestosBase_create'),
    path('presupuestosBase/update/<int:pk>/', PresupuestosBaseUpdateView.as_view(), name='presupuestosBase_update'),
    path('presupuestosBase/delete/<int:pk>/', PresupuestosBaseDeleteView.as_view(), name='presupuestosBase_delete'),
    path('presupuestosBase/pdf/<int:pk>/', PresupuestosBasePdfView.as_view(), name='presupuestosBase_pdf'),
]