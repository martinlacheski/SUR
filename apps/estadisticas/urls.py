from django.urls import path

from apps.estadisticas.views import *

app_name = 'estadisticas'

urlpatterns = [
    # Estadisticas
    path('estadisticas/trabajos_ventas/', TrabajosVentasView.as_view(), name='trabajos_ventas'),
    path('estadisticas/productos_servicios/', ProductosServiciosView.as_view(), name='productos_servicios'),
    path('estadisticas/clientes_trabajos/', ClientesTrabajosView.as_view(), name='clientes_trabajos'),
    path('estadisticas/modelos_mas_realizados/', ModelosMasRealizadosView.as_view(), name='modelos_mas_realizados'),
    path('estadisticas/productos_mas_vendidos/', ProductosMasVendidosView.as_view(), name='productos_mas_vendidos'),
    path('estadisticas/servicios_mas_realizados/', ServiciosMasRealizadosView.as_view(), name='servicios_mas_realizados'),
    path('estadisticas/insumos_mas_utilizados/', InsumosMasUtilizadosView.as_view(), name='insumos_mas_utilizados'),
]
