"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import environ
import os

# Para obtener contraseña y dirección de correo (archivo .env dentro de config/)
env = environ.Env()
environ.Env.read_env()

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

# ALLOWED_HOSTS = ['localhost', '127.0.0.1']
ALLOWED_HOSTS = ["*"]
ASGI_APPLICATION = 'config.asgi.application'


# Application definition

INSTALLED_APPS = [
    'channels',             # si o si tienen que ir primero. Relacionado a documentación
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Librerias
    'widget_tweaks',
    'django.contrib.humanize',
    'simple_history',
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
    # 'apps.bot_telegram',
    'apps.notif_channel',
    'apps.estadisticas',
    'apps.pedidos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Para las pistas de auditoria. Completar el historia de usuario automaticamente
    'simple_history.middleware.HistoryRequestMiddleware',
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
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'SUR',
    #     'USER': 'postgres',
    #     'PASSWORD': 'cli13',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # }
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
TIME_ZONE = 'America/Argentina/Buenos_Aires'

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

CRONJOBS = [
    ('0 8 * * *', 'apps.bot_telegram.cron.rastreoTrabajos'),
    #('0 8 * * 1', 'apps.erp.cron.generarSolicitudPedido'),
]


#DATE_FORMAT = '%d-%m-%y'
# DATE_INPUT_FORMATS = '%d-%m-%Y'
# DATETIME_INPUT_FORMATS = ['%d/%m/%Y %H:%M:%S']

# Necesarios
APSCHEDULER_DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

DJANGO_SETTINGS_MODULE = 'config.settings'


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'surexpress.posadas@gmail.com'
EMAIL_HOST_PASSWORD = 'yfediuvbwddaztqq'