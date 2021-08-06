from django.urls import path

from app.apps.home.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]