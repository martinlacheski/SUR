from django.urls import path

from apps.usuarios.views.tiposUsuarios.views import TiposUsuariosListView, TiposUsuariosCreateView, \
    TiposUsuariosUpdateView, TiposUsuariosDeleteView
from apps.usuarios.views.usuarios.views import UsuariosListView, UsuariosCreateView, UsuariosUpdateView, \
    UsuariosDeleteView

app_name = 'usuarios'

urlpatterns = [
    #Usuarios
    path('usuarios/list/', UsuariosListView.as_view(), name='usuarios_list'),
    path('usuarios/add/', UsuariosCreateView.as_view(), name='usuarios_create'),
    path('usuarios/update/<int:pk>/', UsuariosUpdateView.as_view(), name='usuarios_update'),
    path('usuarios/delete/<int:pk>/', UsuariosDeleteView.as_view(), name='usuarios_delete'),

    # Tipos de Usuarios
    path('usuarios/tipos/list/', TiposUsuariosListView.as_view(), name='tipos_usuarios_list'),
    path('usuarios/tipos/add/', TiposUsuariosCreateView.as_view(), name='tipos_usuarios_create'),
    path('usuarios/tipos/update/<int:pk>/', TiposUsuariosUpdateView.as_view(), name='tipos_usuarios_update'),
    path('usuarios/tipos/delete/<int:pk>/', TiposUsuariosDeleteView.as_view(), name='tipos_usuarios_delete'),

]
