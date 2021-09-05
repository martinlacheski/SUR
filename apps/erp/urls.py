from apps.erp.views.categorias.views import *
from apps.erp.views.productos.views import *
from apps.erp.views.subcategorias.views import *
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
]
