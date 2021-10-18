# chat/urls.py
from django.urls import path

from . import views

#Las URL se van a llamar dentro del body. No importa cual tenga.
# es mas. Probablemente no se use este urls.py
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]