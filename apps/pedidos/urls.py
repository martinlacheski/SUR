from django.urls import path

from apps.pedidos.views.pedidos.views import *
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
    path('pedidos/realizados/pdf/<int:pk>/', PedidoRealizadoPdfView.as_view(), name='pedido_realizado_pdf'),
    # Visualizacion de la confirmación para modificar, confirmar o cancelar un PEDIDO
    path('pedidos/confirm/<int:pk>/', PedidosConfirmView.as_view(), name='pedidos_solicitudes_confirm'),
    path('pedidos/delete/<int:pk>/', PedidosDeleteView.as_view(), name='pedidos_solicitudes_delete'),
    # Solicitudes de Pedidos Vista de Proveedores
    path('pedidos/solicitudes/proveedores/list/', PedidosSolicitudProveedoresListView.as_view(), name='pedidos_solicitudes_proveedores_list'),
    path('pedidos/solicitudes/proveedores/<slug:hash_code>', PedidosSolicitudProveedoresCreateView.as_view(), name='pedidos_solicitudes_proveedores_create'),
    path('pedidos/solicitudes/enviado/', CorrectoSolicitudProveedorView.as_view(), name='pedidos_solicitudes_correcto'), # REDIRIGIR EL REENVIO CORRECTO
    path('pedidos/solicitudes/expired/', ExpiredSolicitudProveedorView.as_view(), name='pedidos_solicitudes_expired'), # REDIRIGIR EL REENVIO SI VENCIÓ
    # Pedidos
    path('pedidos/list/', PedidosListView.as_view(), name='pedidos_list'),
    path('pedidos/pdf/<int:pk>/', PedidosPdfView.as_view(), name='pedidos_pdf'),
]
