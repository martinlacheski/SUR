# Django
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


# Telegram
from typing import Union, List
import logging
from telegram.ext import Updater
import telegram
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import CallbackQuery

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

#       *** NOTIFICAR TRABAJO FINALIZADO ***
def notificarCliente(trabajo):
    bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')
    cliente = Clientes.objects.get(pk=trabajo.cliente_id)
    mensaje = "Hola! 👋 Te informo que tu trabajo con Nro° " + str(trabajo.id) + " se encuentra FINALIZADO.\n\n"
    if trabajo.observaciones:
        mensaje += "📝 Algunas observaciones son: " + str(trabajo.observaciones) + "\n\n"
    mensaje += "💰 El importe a abonar es: $" + str(trabajo.total) + " pesos.\n\n"
    mensaje += "Te pido que indiques cuándo lo vas a pasar a buscar presionando cualquiera de los siguiente botones."
    bot.send_message(chat_id=cliente.chatIdCliente, text=mensaje)

    # Callback data
    data_hoy = {
        'hoy': str(timezone.now().date),
        'cliente': str(cliente.id),
        'trabajo': str(trabajo.id),

    }
    sig_habil = {
        'sig_dia_habil': str(dia_habil_siguiente(timezone.now().date())),
        'cliente': str(cliente.id),
        'trabajo': str(trabajo.id),

    }
    se_comunica = {
        'se_secomunica': 'Se comunicará luego.'
    }
    keyboard = [
        [InlineKeyboardButton("Hoy", callback_data=str(data_hoy))],
        [InlineKeyboardButton("Siguiente día hábil", callback_data=str(sig_habil))],
        [InlineKeyboardButton("Me comunico luego", callback_data=str(se_comunica))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=cliente.chatIdCliente, text="Opciones:\n", reply_markup=reply_markup)

class Command(BaseCommand):
    def handle(self, *args, **options):
        bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')

        #       *** REGISTRO USUARIO ***
        def registroUsuario(update, context):
            if check_chatid_cliente(update.message.from_user.id):
                update.message.reply_text("🛑 No podes registrar tu cuenta de esta manera.")
            else:
                if len(context.args) == 0:
                    update.message.reply_text(text="Hola\! 👋 Este es el registro de usuarios de SUR EXPRESS\.\n\n"
                                                   "Para registrarte, interactuar conmigo y recibir notificaciones"
                                                   " ingresá el comando  */registroUsuario* y a continuación tu nombre"
                                                   " de usuario seguido de tu contraseña\.\nPor ejemplo: \n\n"
                                                   "``` /registroUsuario juan miContraseña ``` \n\n"
                                                   "Luego enviá el mensaje\."
                                              ,parse_mode=telegram.ParseMode.MARKDOWN_V2)
                elif len(context.args) == 2:
                    usuario = context.args[0]
                    password = context.args[1]
                    try:
                        user = Usuarios.objects.get(username=usuario)
                        if user.check_password(password):
                            update.message.reply_text("👌 ¡Todo correcto! Ya podes interactuar conmigo\n\n"
                                                      "⚠ Por una cuestión de seguridad, me tomé el "
                                                      "trabajo de borrar el msj en donde pones tu contraseña.\n\n"
                                                      "🧠 Esta es mi lista de comandos y lo que soy capaz de hacer: ")
                            # TO-do acá van las funcionalidades que hará el bot para los usuarios registrados
                            bot.delete_message(update.message.chat.id, update.message.message_id)
                            user.chatIdUsuario = int(update.message.from_user.id)
                            user.save()
                        else:
                            update.message.reply_text("🚫 Usuario o contraseña incorrecta.\n\n"
                                                      "👍 Volvé a ingresar el comando y asegurate que ambos datos esten"
                                                      " escritos correctamente.")
                    except:
                        update.message.reply_text("🚫 Usuario o contraseña incorrecta.\n\n"
                                                  "👍 Volvé a ingresar el comando y asegurate que ambos datos esten"
                                                  " escritos correctamente.")
                elif len(context.args) != 0 and len(context.args) != 2:
                    update.message.reply_text(text="No ingresaste bien el comando 😅\nRecordá que tiene que ser similar "
                                                   "a\n\n ``` /registroUsuario juan miContraseña ``` "
                                              ,parse_mode=telegram.ParseMode.MARKDOWN_V2)

        #       *** REGISTRO CLIENTE ***
        def registroCliente(update, context):
            # Comprobamos si el cliente trata de registrarse como un usuario.
            if check_chatid_user(update.message.from_user.id):
                update.message.reply_text("🛑 No podes registrar tu cuenta de esta manera. Ya estas registrado.")
            else:
                if len(context.args) == 0:
                    update.message.reply_text(text="Hola\! 👋 Este es el registro de clientes de SUR EXPRESS\.\n\n"
                                                   "Para registrarte y recibir notificaciones ingresá el comando"
                                                   " */registroCliente* y a continuación tu CUIL/CUIT sin guiones o "
                                                   "comas\."
                                                   "\nPor ejemplo: \n\n ``` /registroCliente 20346735739 ``` \n\n"
                                                   "Luego enviá el mensaje\."
                                              ,parse_mode=telegram.ParseMode.MARKDOWN_V2)
                elif len(context.args) == 1:
                    cuil_cuit = context.args[0]

                    # Chequeamos que el cuil/cuit esté correcto
                    # TO-DO acá debe ir comprobación de CUIL con calculadora
                    if cuil_cuit.isdigit() and len(cuil_cuit) == 11:
                        try:
                            cliente = Clientes.objects.get(cuil=cuil_cuit)
                            cliente.chatIdCliente = int(update.message.from_user.id)
                            cliente.save()
                            update.message.reply_text("¡Todo correcto! 👌\n\nVas a recibir una notificación cuando alguno "
                                                      "de tus trabajos esté listo.")

                            # Si el cliente ya tiene trabajos, ni bien se registra se los mandamos
                            trabajosCliente = Trabajos.objects.filter(cliente=cliente)
                            if trabajosCliente:
                                update.message.reply_text(mandarTrabajos(trabajosCliente))
                        except ObjectDoesNotExist:
                            # El cliente no estaba registrado.
                            update.message.reply_text("Mmm, esto es raro 🤔 \n\n"
                                                      "No te encontramos registrado como cliente."
                                                      " Este inconveniente será reportado!\n")
                            clienteNoRegistrado(cuil_cuit, update.message.from_user.username,
                                                update.message.from_user.first_name)  # Registramos el incidente

                            # Se lo notificamos a todos los usuarios seteados que tengan chatID
                            usersToNotif = notifIncidentesUsuarios.objects.all()
                            for user in usersToNotif:
                                if user.usuario_id.chatIdUsuario:
                                    bot.send_message(text="Hola! 😌\nTe informo que un cliente intentó registrarse y "
                                                          "su CUIL/CUIT no estaba registrado.\n\n\n Sus datos son: \n\n"
                                                          "CUIL/CUIT: " + cuil_cuit + "\n Usuario en Telegram: " +
                                                           str(update.message.from_user.username) + "\nNombre en Telegram: " +
                                                           str(update.message.from_user.first_name),
                                                           chat_id=user.usuario_id.chatIdUsuario)
                    else:
                        update.message.reply_text("CUIL/CUIT ingresado contiene letras o no tiene una"
                                                  " longitud de 11 caracteres")
                elif len(context.args) != 0 and len(context.args) != 1:
                    update.message.reply_text(text="No ingresaste bien el comando 😅\nRecordá que tiene que ser similar "
                                                   "a\n\n ``` /registroCliente 20346735739 ``` "
                                              ,parse_mode=telegram.ParseMode.MARKDOWN_V2)

        # Procesa todas las respuestas en botones en los mensajes
        def button(update, context):
            query = update.callback_query
            # Vemos quién nos respondió y acorde a ello hacemos cosas
            try:
                cliente = Clientes.objects.get(chatIdCliente=update.effective_chat.id)
                eleccion_retiro = query.data
                query.answer()
                estado_retiro = registrarRetiro(eleccion_retiro)
                if estado_retiro['proc']:
                    # Le repondemos al cliente.
                    query.edit_message_text(text="👍 Tu respuesta ha sido registrada y notificada al personal"
                                                 " de SUR EXPRESS")
                    # Avisamos a los administradores por télegram
                    usersToNotif = notifIncidentesUsuarios.objects.all()
                    mensaje = estado_retiro['respuesta_bot']
                    for user in usersToNotif:
                        if user.usuario_id.chatIdUsuario:
                            bot.send_message(text=str(mensaje), chat_id=user.usuario_id.chatIdUsuario)

                    # Avisamos a los administradores por Sistema.
                    eleccion_retiro = ast.literal_eval(eleccion_retiro)
                    titulo = "Respuesta de Cliente - Trabajo Nro " + str(eleccion_retiro['trabajo']) + "."
                    notificarSistema(titulo, estado_retiro['respuesta_sist'])
                else:
                    mensaje = estado_retiro['respuesta']
                    query.edit_message_text(text=mensaje)
            except ObjectDoesNotExist:
                try:
                    usuario = Usuarios.objects.get(chatIdUsuario=update.effective_chat.id)
                    opciones = ['ventasDia', 'comprasDia', 'trabajosPlanif', 'trabajosDia']
                    # Bloque ejecutado si se trata de proc automatizado de consulta gerencial
                    if query.data in opciones:
                        #TO - DO: acá solamente usuarios gerenciales pueden acceder
                        mensaje = generarReporte(query.data)
                        hoy = timezone.now().date()
                        print(str(hoy.strftime('%d\-%m\-%Y')))
                        if mensaje['tipo'] == 'venta':
                            bot.send_message(text="Este es el reporte que solicitaste\!\n\n ⬆ Ventas al día de la fecha " +
                                                    str(hoy.strftime('%d\-%m\-%Y')) + "\n\n"
                                                  "``` TOTAL\: \$``` " + str(int(mensaje['totalDia'])) + " pesos\n" +
                                                  "``` Total productos\: \$``` " + str(int(mensaje['totalProductos'])) + " pesos\n" +
                                                  "``` Total servicios\: \$``` " + str(int(mensaje['totalServicios'])) + " pesos\n" +
                                                  "``` Cant\. ventas\: ``` " + str(int(mensaje['cantVentas'])) + "\n",
                                                    parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                                    chat_id=usuario.chatIdUsuario)
                        if mensaje['tipo'] == "compra":
                            bot.send_message(text="Este es el reporte que solicitaste\!\n\n ⬇ Compras al día de la fecha " +
                                                  str(hoy.strftime('%d\-%m\-%Y')) + "\n\n"
                                                  "``` TOTAL\: \$``` " + str(int(mensaje['totalDia'])) + " pesos\n" +
                                                  "``` Total productos\: \$``` " + str(int(mensaje['totalProductos'])) + " pesos\n" +
                                                  "``` Cant\. compras\: ``` " + str(int(mensaje['cantCompras'])) + "\n",
                                             parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                             chat_id=usuario.chatIdUsuario)
                        if mensaje['tipo'] == "trabajosPlanif":
                            bot.send_message(text="Este es el reporte que solicitaste!\n\n 📅 Estado de trabajos para"
                                                  " planificación desde " + mensaje['planifDesde'] + " hasta " +
                                                  mensaje['planifHasta'] + "\n\n" + mensaje['mensaje'],
                                            chat_id=usuario.chatIdUsuario)
                        if mensaje['tipo'] == "trabajosDia":
                            bot.send_message(text="Este es el reporte que solicitaste!\n\n 🛠️ Nuevos trabajos ingresados" 
                                                  " hoy " + str(hoy.strftime('%d-%m-%Y')) + "\n\n" + mensaje['mensaje'],
                                             chat_id=usuario.chatIdUsuario)
                    else:
                        # Bloque ejecutado por proc auto de asiganción de trabajos
                        resp_to_dict = ast.literal_eval(query.data)
                        t = Trabajos.objects.get(pk=resp_to_dict['trabajo'])
                        seg = seguimientoTrabajos.objects.get(trabajo=t)
                        response = almacenarRespuesta(resp_to_dict)
                        # Notificamos inmediatamente al sistema que alguien respondió "Faltan repuestos".
                        if 'Faltan repuestos' in response:
                            titulo = "Faltan repuestos para un trabajo estancado"
                            descripcion = "Usuario " + str(seg.trabajo.usuarioAsignado.username) + " ha indicado que" \
                                          " faltan repuestos para el trabajo Nro° " + str(t.id) + "."
                            notificarSistema(titulo, descripcion)
                        query.edit_message_text(text=response)


                except ObjectDoesNotExist:
                    print("no está registrado")

        # Procesa los mensajes que NO son comandos.
        def respuestaDefault(update, context):
            msjRecibido = str(update.message.text).upper()

            try:
                user_gerencial = Usuarios.objects.get(chatIdUsuario=update.effective_chat.id)
                esUser = True
            except ObjectDoesNotExist:
                try:
                    cliente = Clientes.objects.get(chatIdCliente=update.effective_chat.id)
                    esUser = False
                except ObjectDoesNotExist:
                    bot.send_message(chat_id=update.effective_chat.id,
                                     text="No tenes permiso para interactuar conmigo.")
                    personaNoRegistrada(update.message.from_user.username, update.message.from_user.first_name)

            # palabras que puede usar un user
            if esUser:
                if msjRecibido == 'REPORTAME':
                    botones = armarBotonesConsulta()
                    bot.send_message(chat_id=user_gerencial.chatIdUsuario, text="📈 Estos son los "
                                     "reportes que tengo disponibles para vos\n", reply_markup=botones)
                else:
                    update.message.reply_text(text=str(user_gerencial.username) + " no entendí lo que dijiste 🤨\n"
                                              "Recordá que únicamente respondo a la palabra:\n\n ```reportame``` \n\n"
                                              " la cual tenes que enviar en un único mensaje\.",
                                              parse_mode=telegram.ParseMode.MARKDOWN_V2)

            # Palabras que puede usar un cliente
            else:
                if msjRecibido == 'TRABAJOS':
                    trabajosCliente = Trabajos.objects.filter(cliente=cliente)
                    if trabajosCliente:
                        update.message.reply_text(mandarTrabajos(trabajosCliente))
                    else:
                        update.message.reply_text("Hola " + str(cliente.razonSocial) + "👋!\n"
                                                   "😅Todavía no tenemos registrado ningún trabajo a tu nombre.")
                else:
                    update.message.reply_text(text=str(cliente.razonSocial) + " no entendí lo que dijiste 🤨\n"
                                              "Recordá que únicamente respondo a la palabra:\n\n ```trabajos``` \n\n"
                                              " la cual tenes que enviar en un único mensaje\."
                                              ,parse_mode=telegram.ParseMode.MARKDOWN_V2)




        # Token
        updater = Updater(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM', use_context=True)
        dispatcher = updater.dispatcher

        # Debugger
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        # ** COMANDOS **
        start_handler = CommandHandler('registroCliente', registroCliente)
        start_handler2 = CommandHandler('registroUsuario', registroUsuario)
        start_handler4 = MessageHandler(Filters.text & (~Filters.command), respuestaDefault)
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(start_handler2)
        dispatcher.add_handler(start_handler4)
        dispatcher.add_handler(CallbackQueryHandler(button))
        updater.start_polling()