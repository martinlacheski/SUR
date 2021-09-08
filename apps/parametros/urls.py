from django.urls import path

from apps.parametros.views.condicionesIVA.views import *
from apps.parametros.views.tiposIVA.views import *

app_name = 'parametros'

urlpatterns = [
    #Tipos de IVA
    path('tipo-iva/list/', TiposIVAListView.as_view(), name='tiposIVA_list'),
    path('tipo-iva/add/', TiposIVACreateView.as_view(), name='tiposIVA_create'),
    path('tipo-iva/update/<int:pk>/', TiposIVAUpdateView.as_view(), name='tiposIVA_update'),
    path('tipo-iva/delete/<int:pk>/', TiposIVADeleteView.as_view(), name='tiposIVA_delete'),
    #Tipos de IVA
    path('condicion-iva/list/', CondicionesIVAListView.as_view(), name='condicionesIVA_list'),
    path('condicion-iva/add/', CondicionesIVACreateView.as_view(), name='condicionesIVA_create'),
    path('condicion-iva/update/<int:pk>/', CondicionesIVAUpdateView.as_view(), name='condicionesIVA_update'),
    path('condicion-iva/delete/<int:pk>/', CondicionesIVADeleteView.as_view(), name='condicionesIVA_delete'),

]