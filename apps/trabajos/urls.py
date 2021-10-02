from django.urls import path

from apps.trabajos.views.trabajos.views import *

app_name = 'trabajos'

urlpatterns = [
    # Trabajos
    path('trabajos/list/', TrabajosListView.as_view(), name='trabajos_list'),
    path('trabajos/add/', TrabajosCreateView.as_view(), name='trabajos_create'),
    path('trabajos/update/<int:pk>/', TrabajosUpdateView.as_view(), name='trabajos_update'),
    path('trabajos/confirm/<int:pk>/', TrabajosConfirmView.as_view(), name='trabajos_confirm'),
    path('trabajos/deliver/<int:pk>/', TrabajosDeliverView.as_view(), name='trabajos_deliver'),
    path('trabajos/delete/<int:pk>/', TrabajosDeleteView.as_view(), name='trabajos_delete'),
    path('trabajos/pdf/<int:pk>/', TrabajosPdfView.as_view(), name='trabajos_pdf'),
]