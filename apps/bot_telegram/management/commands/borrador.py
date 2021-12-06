# Django
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.models import Group, Permission



# Telegram
from typing import Union, List
import logging
from telegram.ext import Updater
import telegram


# Models
from apps.usuarios.models import Usuarios
from apps.erp.models import Clientes
from apps.bot_telegram.models import *
from apps.bot_telegram.logicaBot import *
from apps.trabajos.models import Trabajos

# Otros
import datetime
import ast
from apps.notif_channel.consumers import notificationConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync




class Command(BaseCommand):
    def handle(self, *args, **options):
        trabajo = Trabajos.objects.get(pk=38)
        bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')
        cliente = Clientes.objects.get(pk=trabajo.cliente_id)
        mensaje = "Hola! 👋 Te informo que tu trabajo con Nro° " + str(trabajo.id) + " se encuentra FINALIZADO.\n\n"
        if trabajo.observaciones:
            mensaje += "📝 Algunas observaciones son: " + str(trabajo.observaciones) + "\n\n"
        mensaje += "💰 El importe a abonar es: $" + str(trabajo.total) + " pesos.\n\n"
        mensaje += "Te pido que indiques cuándo lo vas a pasar a buscar presionando cualquiera de los siguiente botones."
        if cliente.chatIdCliente:
            bot.send_message(chat_id=cliente.chatIdCliente, text=mensaje)

            # Callback data
            data_hoy = {'hoy': str(timezone.now()), 'cliente': str(cliente.id), 'trabajo': str(trabajo.id)}
            sig_habil = {'sig_dia_habil': str(datetime.date.today()), 'cliente': str(cliente.id),
                         'trabajo': str(trabajo.id)}
            se_comunica = {'se_secomunica': 'Se comunicará luego.'}
            print(len(str(data_hoy).encode('utf-8')))
            print(len(str(sig_habil).encode('utf-8')))
            print(len(str(se_comunica).encode('utf-8')))

            keyboard = [
                [InlineKeyboardButton("Hoy", callback_data=str(data_hoy))],
                [InlineKeyboardButton("Siguiente día hábil", callback_data=str(sig_habil))],
                [InlineKeyboardButton("Me comunico luego", callback_data=str(se_comunica))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=cliente.chatIdCliente, text="Opciones:\n", reply_markup=reply_markup)
        else:
            titulo = "Notificación a cliente fallida"
            descripcion = "Se intentó notificar al cliente " + str(cliente.razonSocial) + " sin éxito" \
                                                                                          " ya que el mismo no está registrado con el BOT."

            #notificarSistema(titulo, descripcion)
            print("no tiene chat id")


def mensaje():
    mensaje = "Hola! 👋 Te informo que el trabajo Nro° 34 \n\n" + \
              "Marca: FORD \n" + "Modelo: FIESTA, ECOSPORT, KA \n\n" + \
              "No está finalizado según la prioridad establecida.\n"
    return mensaje