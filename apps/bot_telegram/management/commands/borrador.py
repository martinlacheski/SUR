from django.utils import timezone
import datetime
import random
import telegram
from apscheduler.schedulers.background import BlockingScheduler
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from apps.bot_telegram.logicaBot import porcentajeTrabajo, notificarSistema
from apps.bot_telegram.models import seguimientoTrabajos
from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos, DetalleServiciosTrabajo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.db.models import Count
from apps.usuarios.models import Usuarios
from apps.bot_telegram.logicaBot import porcentajeTrabajo
#from apps.usuarios.models import TiposUsuarios
from django.core.mail import EmailMultiAlternatives
from django.conf import settings





class Command(BaseCommand):
    def handle(self, *args, **options):
        subject, from_email, to = 'prueba',settings.EMAIL_HOST_USER , 'leoquiroga221@gmail.com'
        text_content = 'This is an important message.'
        html_content = '<p>This is an <strong>important</strong> message.</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def mensaje():
    mensaje = "Hola! 👋 Te informo que el trabajo Nro° 34 \n\n" + \
              "Marca: FORD \n" + "Modelo: FIESTA, ECOSPORT, KA \n\n" + \
              "No está finalizado según la prioridad establecida.\n"
    return mensaje