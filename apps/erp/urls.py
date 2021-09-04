from apps.erp.views.categorias.views import *
from django.urls import path

app_name = 'erp'

urlpatterns = [
    # CATEGORIAS
    path('categorias/list/', CategoriasListView.as_view(), name='categorias_list'),
    path('categorias/add/', CategoriasCreateView.as_view(), name='categorias_create'),
    path('categorias/update/<int:pk>/', CategoriasUpdateView.as_view(), name='categorias_update'),
    path('categorias/delete/<int:pk>/', CategoriasDeleteView.as_view(), name='categorias_delete'),
    # #Provincias
    # path('provincias/list/', ProvinciasListView.as_view(), name='provincias_list'),
    # path('provincias/add/', ProvinciasCreateView.as_view(), name='provincias_create'),
    # path('provincias/update/<int:pk>/', ProvinciasUpdateView.as_view(), name='provincias_update'),
    # path('provincias/delete/<int:pk>/', ProvinciasDeleteView.as_view(), name='provincias_delete'),
    # #Localidades
    # path('localidades/list/', LocalidadesListView.as_view(), name='localidades_list'),
    # path('localidades/add/', LocalidadesCreateView.as_view(), name='localidades_create'),
    # path('localidades/update/<int:pk>/', LocalidadesUpdateView.as_view(), name='localidades_update'),
    # path('localidades/delete/<int:pk>/', LocalidadesDeleteView.as_view(), name='localidades_delete'),
]
