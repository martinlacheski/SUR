from django.urls import path

from apps.parametros.views.condicionesIVA.views import *
from apps.parametros.views.condicionesPago.views import *
from apps.parametros.views.estados.views import *
from apps.parametros.views.marcas.views import *
from apps.parametros.views.modelos.views import *
from apps.parametros.views.prioridades.views import *
from apps.parametros.views.tiposComprobante.views import *
from apps.parametros.views.tiposIVA.views import *
from apps.parametros.views.tiposPercepciones.views import *

app_name = 'parametros'

urlpatterns = [
    #Tipos de IVA
    path('tipos-iva/list/', TiposIVAListView.as_view(), name='tiposIVA_list'),
    path('tipos-iva/add/', TiposIVACreateView.as_view(), name='tiposIVA_create'),
    path('tipos-iva/update/<int:pk>/', TiposIVAUpdateView.as_view(), name='tiposIVA_update'),
    path('tipos-iva/delete/<int:pk>/', TiposIVADeleteView.as_view(), name='tiposIVA_delete'),
    #condiciones frente al IVA
    path('condiciones-iva/list/', CondicionesIVAListView.as_view(), name='condicionesIVA_list'),
    path('condiciones-iva/add/', CondicionesIVACreateView.as_view(), name='condicionesIVA_create'),
    path('condiciones-iva/update/<int:pk>/', CondicionesIVAUpdateView.as_view(), name='condicionesIVA_update'),
    path('condiciones-iva/delete/<int:pk>/', CondicionesIVADeleteView.as_view(), name='condicionesIVA_delete'),
    #Tipos de Percepciones
    path('tipos-percepciones/list/', TiposPercepcionesListView.as_view(), name='tiposPercepciones_list'),
    path('tipos-percepciones/add/', TiposPercepcionesCreateView.as_view(), name='tiposPercepciones_create'),
    path('tipos-percepciones/update/<int:pk>/', TiposPercepcionesUpdateView.as_view(), name='tiposPercepciones_update'),
    path('tipos-percepciones/delete/<int:pk>/', TiposPercepcionesDeleteView.as_view(), name='tiposPercepciones_delete'),
    #Condiciones de Pago
    path('condiciones-pago/list/', CondicionesPagoListView.as_view(), name='condicionesPago_list'),
    path('condiciones-pago/add/', CondicionesPagoCreateView.as_view(), name='condicionesPago_create'),
    path('condiciones-pago/update/<int:pk>/', CondicionesPagoUpdateView.as_view(), name='condicionesPago_update'),
    path('condiciones-pago/delete/<int:pk>/', CondicionesPagoDeleteView.as_view(), name='condicionesPago_delete'),
    #Tipos de Comprobantes
    path('tipos-comprobante/list/', TiposComprobantesListView.as_view(), name='tiposComprobantes_list'),
    path('tipos-comprobante/add/', TiposComprobantesCreateView.as_view(), name='tiposComprobantes_create'),
    path('tipos-comprobante/update/<int:pk>/', TiposComprobantesUpdateView.as_view(), name='tiposComprobantes_update'),
    path('tipos-comprobante/delete/<int:pk>/', TiposComprobantesDeleteView.as_view(), name='tiposComprobantes_delete'),
    #Marcas
    path('marcas/list/', MarcasListView.as_view(), name='marcas_list'),
    path('marcas/add/', MarcasCreateView.as_view(), name='marcas_create'),
    path('marcas/update/<int:pk>/', MarcasUpdateView.as_view(), name='marcas_update'),
    path('marcas/delete/<int:pk>/', MarcasDeleteView.as_view(), name='marcas_delete'),
    #Modelos
    path('modelos/list/', ModelosListView.as_view(), name='modelos_list'),
    path('modelos/add/', ModelosCreateView.as_view(), name='modelos_create'),
    path('modelos/update/<int:pk>/', ModelosUpdateView.as_view(), name='modelos_update'),
    path('modelos/delete/<int:pk>/', ModelosDeleteView.as_view(), name='modelos_delete'),
    #Estados de Trabajos
    path('estados-trabajo/list/', EstadosListView.as_view(), name='estados_list'),
    path('estados-trabajo/add/', EstadosCreateView.as_view(), name='estados_create'),
    path('estados-trabajo/update/<int:pk>/', EstadosUpdateView.as_view(), name='estados_update'),
    path('estados-trabajo/delete/<int:pk>/', EstadosDeleteView.as_view(), name='estados_delete'),
    #Prioridades de Trabajos
    path('prioridades-trabajos/list/', PrioridadesListView.as_view(), name='prioridades_list'),
    path('prioridades-trabajos/add/', PrioridadesCreateView.as_view(), name='prioridades_create'),
    path('prioridades-trabajos/update/<int:pk>/', PrioridadesUpdateView.as_view(), name='prioridades_update'),
    path('prioridades-trabajos/delete/<int:pk>/', PrioridadesDeleteView.as_view(), name='prioridades_delete'),
]