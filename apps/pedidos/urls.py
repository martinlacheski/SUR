from django.urls import path

from apps.pedidos.views.pedidosSolicitud.views import *
from apps.pedidos.views.pedidosSolicitudProveedores.views import *

app_name = 'pedidos'

urlpatterns = [
    # Solicitudes de Pedidos
    path('pedidos/solicitudes/list/', PedidosSolicitudListView.as_view(), name='pedidos_solicitudes_list'),
    path('pedidos/solicitudes/add/', PedidosSolicitudCreateView.as_view(), name='pedidos_solicitudes_create'),
    path('pedidos/solicitudes/update/<int:pk>/', PedidosSolicitudUpdateView.as_view(), name='pedidos_solicitudes_update'),
    path('pedidos/solicitudes/confirm/<int:pk>/', PedidosSolicitudConfirmView.as_view(), name='pedidos_solicitudes_confirm'),
    path('pedidos/solicitudes/delete/<int:pk>/', PedidosSolicitudDeleteView.as_view(), name='pedidos_solicitudes_delete'),
    path('pedidos/solicitudes/pdf/<int:pk>/', PedidosSolicitudPdfView.as_view(), name='pedidos_solicitudes_pdf'),
    # Solicitudes de Pedidos Vista de Proveedores
    path('pedidos/solicitudes/proveedores/list/', PedidosSolicitudProveedoresListView.as_view(), name='pedidos_solicitudes_proveedores_list'),
    path('pedidos/solicitudes/proveedores/<slug:hash_code>', PedidosSolicitudProveedoresCreateView.as_view(), name='pedidos_solicitudes_proveedores_create'),
    path('pedidos/solicitudes/enviado/', CorrectoSolicitudProveedorView.as_view(), name='pedidos_solicitudes_correcto'), # REDIRIGIR EL REENVIO CORRECTO
    path('pedidos/solicitudes/expired/', ExpiredSolicitudProveedorView.as_view(), name='pedidos_solicitudes_expired'), # REDIRIGIR EL REENVIO SI VENCIÓ
]
