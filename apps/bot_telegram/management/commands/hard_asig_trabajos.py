from django.core.management.base import BaseCommand, CommandError
from apps.trabajos.models import Trabajos
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
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        i = 0
        bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')
        trabajo = Trabajos.objects.get(pk=39)
        trabajo.usuarioAsignado = Usuarios.objects.get(pk=1)
        trabajo.save()
        # Se envia 3 veces el aviso
        while i < 3:
            bot.send_message(chat_id=1241934509, text=mensaje(trabajo))
            faltan_repuestos = {}
            postergar = {}
            keyboard = [
                [InlineKeyboardButton("🛠 Faltan repuestos", callback_data=str(faltan_repuestos))],
                [InlineKeyboardButton("🕙 Postergar", callback_data=str(postergar))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=1241934509,
                             text="Elegí una opción: \n",
                             reply_markup=reply_markup)
            i += 1
            time.sleep(3)

        time.sleep(2)
        # re-asigna el trabajo
        trabajo.usuarioAsignado = Usuarios.objects.get(pk=5)
        trabajo.save()

        # Notifica a usuario que perdió el trabajo
        bot.send_message(chat_id=1241934509,
                         text="🔴 Por falta de respuesta he reasignado tu trabajo Nro° " + str(trabajo.id) +\
                                                                 ". El mismo ya no será tu responsabilidad.")

        # Notifica al usuario que "ganó" el trabajo.
        bot.send_message(chat_id=630659758,
                         text="⚠ AVISO ⚠ \nTe he asignado el trabajo  Nro° " + str(trabajo.id) +\
                              ". El mismo ya no será tu responsabilidad.")
        # Notifica por sistema
        titulo = "Cambio de asignación de Trabajo"
        descripcion = "El trabajo Nro° " + str(trabajo.id) + " originalmente responsabilidad del usuario martin, fué" \
                                                       " re-asignado al usuario leo"
        notificarSistema(titulo, descripcion)




def mensaje(t):
    mensaje = "Hola! 👋 Te informo que el trabajo Nro°" + str(t.id) + "\n\n" +\
    "Marca: " + str(t.modelo.marca.nombre) + "\n" + "Modelo: " + str(t.modelo.nombre) + "\n\n" +\
    "No está finalizado según la prioridad establecida.\n"
    return mensaje