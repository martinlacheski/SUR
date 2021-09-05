from django.urls import path

from apps.parametros.views.tiposIVA.views import *

app_name = 'parametros'

urlpatterns = [
    #Tipos de IVA
    path('iva/list/', TiposIVAListView.as_view(), name='tiposIVA_list'),
    path('iva/add/', TiposIVACreateView.as_view(), name='tiposIVA_create'),
    path('iva/update/<int:pk>/', TiposIVAUpdateView.as_view(), name='tiposIVA_update'),
    path('iva/delete/<int:pk>/', TiposIVADeleteView.as_view(), name='tiposIVA_delete'),
]