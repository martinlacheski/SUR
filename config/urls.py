"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('apps.login.urls')),
    path('', include('apps.login.urls')),
    path('', include('apps.home.urls')),
    path('', include('apps.parametros.urls')),
    path('', include('apps.geografico.urls')),
    path('', include('apps.usuarios.urls')),
    path('', include('apps.erp.urls')),
    path('', include('apps.presupuestos.urls')),
    path('', include('apps.trabajos.urls')),
    path('', include('apps.agenda.urls')),
    path('', include('apps.bot_telegram.urls')),
    path('', include('apps.notif_channel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

