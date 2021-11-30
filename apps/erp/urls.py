from apps.erp.views.categorias.views import *
from apps.erp.views.clientes.views import *
from apps.erp.views.compras.views import *
from apps.erp.views.pedidosSolicitud.views import *
from apps.erp.views.pedidosSolicitudProveedores.views import *
from apps.erp.views.proveedores.views import *
from apps.erp.views.subcategorias.views import *
from apps.erp.views.productos.views import *
from apps.erp.views.servicios.views import *
from apps.erp.views.ventas.views import *

from django.urls import path

app_name = 'erp'

urlpatterns = [
    # Categorias
    path('categorias/list/', CategoriasListView.as_view(), name='categorias_list'),
    path('categorias/add/', CategoriasCreateView.as_view(), name='categorias_create'),
    path('categorias/update/<int:pk>/', CategoriasUpdateView.as_view(), name='categorias_update'),
    path('categorias/delete/<int:pk>/', CategoriasDeleteView.as_view(), name='categorias_delete'),
    # Subcategorias
    path('subcategorias/list/', SubcategoriasListView.as_view(), name='subcategorias_list'),
    path('subcategorias/add/', SubcategoriasCreateView.as_view(), name='subcategorias_create'),
    path('subcategorias/update/<int:pk>/', SubcategoriasUpdateView.as_view(), name='subcategorias_update'),
    path('subcategorias/delete/<int:pk>/', SubcategoriasDeleteView.as_view(), name='subcategorias_delete'),
    # Productos
    path('productos/list/', ProductosListView.as_view(), name='productos_list'),
    path('productos/add/', ProductosCreateView.as_view(), name='productos_create'),
    path('productos/update/<int:pk>/', ProductosUpdateView.as_view(), name='productos_update'),
    path('productos/delete/<int:pk>/', ProductosDeleteView.as_view(), name='productos_delete'),
    path('productos/audit/', ProductosAuditListView.as_view(), name='productos_audit'),
    # Servicios
    path('servicios/list/', ServiciosListView.as_view(), name='servicios_list'),
    path('servicios/add/', ServiciosCreateView.as_view(), name='servicios_create'),
    path('servicios/update/<int:pk>/', ServiciosUpdateView.as_view(), name='servicios_update'),
    path('servicios/delete/<int:pk>/', ServiciosDeleteView.as_view(), name='servicios_delete'),
    path('servicios/audit/', ServiciosAuditListView.as_view(), name='servicios_audit'),
    # Clientes
    path('clientes/list/', ClientesListView.as_view(), name='clientes_list'),
    path('clientes/add/', ClientesCreateView.as_view(), name='clientes_create'),
    path('clientes/update/<int:pk>/', ClientesUpdateView.as_view(), name='clientes_update'),
    path('clientes/delete/<int:pk>/', ClientesDeleteView.as_view(), name='clientes_delete'),
    # Proveedores
    path('proveedores/list/', ProveedoresListView.as_view(), name='proveedores_list'),
    path('proveedores/add/', ProveedoresCreateView.as_view(), name='proveedores_create'),
    path('proveedores/update/<int:pk>/', ProveedoresUpdateView.as_view(), name='proveedores_update'),
    path('proveedores/delete/<int:pk>/', ProveedoresDeleteView.as_view(), name='proveedores_delete'),
    # Ventas
    path('ventas/list/', VentasListView.as_view(), name='ventas_list'),
    path('ventas/add/', VentasCreateView.as_view(), name='ventas_create'),
    path('ventas/update/<int:pk>/', VentasUpdateView.as_view(), name='ventas_update'),
    path('ventas/delete/<int:pk>/', VentasDeleteView.as_view(), name='ventas_delete'),
    path('ventas/pdf/<int:pk>/', VentasPdfView.as_view(), name='ventas_pdf'),
    path('ventas/audit/', VentasAuditListView.as_view(), name='ventas_audit'),
    # Compras
    path('compras/list/', ComprasListView.as_view(), name='compras_list'),
    path('compras/add/', ComprasCreateView.as_view(), name='compras_create'),
    path('compras/update/<int:pk>/', ComprasUpdateView.as_view(), name='compras_update'),
    path('compras/delete/<int:pk>/', ComprasDeleteView.as_view(), name='compras_delete'),
    path('compras/pdf/<int:pk>/', ComprasPdfView.as_view(), name='compras_pdf'),
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
    path('pedidos/solicitudes/expired/', ExpiredSolicitudProveedorView.as_view(), name='pedidos_solicitudes_expired'),
]
