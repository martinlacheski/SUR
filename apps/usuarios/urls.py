from django.urls import path

from apps.usuarios.views.tiposUsuarios.views import TiposUsuariosListView, TiposUsuariosCreateView, \
    TiposUsuariosUpdateView, TiposUsuariosDeleteView
from apps.usuarios.views.gruposUsuarios.views import *
from apps.usuarios.views.usuarios.views import *

app_name = 'usuarios'

urlpatterns = [
    #Usuarios
    path('usuarios/list/', UsuariosListView.as_view(), name='usuarios_list'),
    path('usuarios/add/', UsuariosCreateView.as_view(), name='usuarios_create'),
    path('usuarios/update/<int:pk>/', UsuariosUpdateView.as_view(), name='usuarios_update'),
    path('usuarios/delete/<int:pk>/', UsuariosDeleteView.as_view(), name='usuarios_delete'),
    # Editar Perfil del Usuario Actual
    path('perfil/', UsuariosPerfilView.as_view(), name='usuario_perfil'),
    # Editar Password del Usuario Actual
    path('change/password/', UsuariosChangePasswordView.as_view(), name='usuario_change_password'),
    # Tipos de Usuarios (se va a ir)
    path('usuarios/tipos/list/', TiposUsuariosListView.as_view(), name='tipos_usuarios_list'),
    path('usuarios/tipos/add/', TiposUsuariosCreateView.as_view(), name='tipos_usuarios_create'),
    path('usuarios/tipos/update/<int:pk>/', TiposUsuariosUpdateView.as_view(), name='tipos_usuarios_update'),
    path('usuarios/tipos/delete/<int:pk>/', TiposUsuariosDeleteView.as_view(), name='tipos_usuarios_delete'),

    # Grupos de Usuarios
    path('usuarios/grupos/list/', GruposUsuariosListView.as_view(), name='grupos_usuarios_list'),
    path('usuarios/grupos/add/', GruposUsuariosCreateView.as_view(), name='grupos_usuarios_create'),
    path('usuarios/grupos/update/<int:pk>/', GruposUsuariosUpdateView.as_view(), name='grupos_usuarios_update'),
    path('usuarios/grupos/delete/<int:pk>/', GruposUsuariosDeleteView.as_view(), name='grupos_usuarios_delete'),

]
