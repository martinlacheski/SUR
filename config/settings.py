"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# Cambiamos por el siguiente:
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gkq$j64h%z-0uoq35u+)5oow6khuw1*f96i_88=d^go6)v$tp+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['localhost', '127.0.0.1']
ASGI_APPLICATION = 'config.asgi.application'


# Application definition

INSTALLED_APPS = [
    'channels',
    'django_cron',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    #Librerias
    'widget_tweaks',
    'django.contrib.humanize',
    # Aplicaciones
    'apps.parametros',
    'apps.login',
    'apps.home',
    'apps.geografico',
    'apps.usuarios',
    'apps.erp',
    'apps.presupuestos',
    'apps.trabajos',
    'apps.agenda',
    'apps.bot_telegram',
    'apps.notif_channel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        # Reemplazamos por el siguiente
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        # Reemplazamos por lo siguiente:
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/



#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-ar'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Carpeta de archivos estaticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Path donde los arhivos seran almacenados
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Base url de los archivos
MEDIA_URL = '/media/'

# Redireccion al Login Correcto
LOGIN_REDIRECT_URL = '/home/'

# Redireccion al logout
LOGOUT_REDIRECT_URL = '/login/'

# Direccion de Login
LOGIN_URL = '/login/'

# Extension Modelo Abstracto Usuarios
AUTH_USER_MODEL = 'usuarios.Usuarios'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Probablemente innecesarios. Si joden, chau
#DATE_FORMAT = '%d-%m-%y'
# DATE_INPUT_FORMATS = '%d-%m-%Y'
# DATETIME_INPUT_FORMATS = ['%d/%m/%Y %H:%M:%S']

# Necesarios
APSCHEDULER_DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

DJANGO_SETTINGS_MODULE = 'config.settings'


CRONJOBS = [
    ('*/1 * * * *', 'apps.agenda.cron.scheduler_eventos')
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
