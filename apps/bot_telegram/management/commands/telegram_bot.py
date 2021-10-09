import datetime
from typing import Union, List
from django.core.management.base import BaseCommand, CommandError
import logging
from telegram.ext import Updater
import telegram
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import CallbackQuery
from apps.usuarios.models import Usuarios
from apps.erp.models import Clientes
from apps.bot_telegram.models import *
from apps.bot_telegram.logicaBot import *

class Command(BaseCommand):



    def handle(self, *args, **options):
        bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')

        print("hola")

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
                                                      "trabajo de borrar el msj en donde pones tu contraseña. No queremos "
                                                      "comprometernos si alguien lee el chat... ¿no?\n\n"
                                                      "🧠 Esta es mi lista de comandos y lo que soy capaz de hacer: ")
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

        def registroCliente(update, context):
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
                    if cuil_cuit.isdigit() and len(cuil_cuit) == 11:
                        try:
                            cliente = Clientes.objects.get(cuil=cuil_cuit)
                            cliente.chatIdCliente = int(update.message.from_user.id)
                            cliente.save()
                            update.message.reply_text("¡Todo correcto! 👌\n\nVas a recibir una notificación cuando alguno "
                                                      "de tus trabajos esté listo.")
                        except:
                            # Le respondemos al cliente
                            update.message.reply_text("Mmm, esto es raro 🤔 \n\n"
                                                      "No te encontramos registrado "
                                                      "como cliente. Este inconveniente será reportado!\n")
                            registrarSuceso(cuil_cuit)  # Registramos el incidente

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

            #if len(context.args) == 2:

        def test(update, context):
            """Sends a message with three inline buttons attached."""
            keyboard = [
                [
                    InlineKeyboardButton("Option 1", callback_data='1'),
                    InlineKeyboardButton("Option 2", callback_data='2'),
                ],
                [InlineKeyboardButton("Option 3", callback_data='3')],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text('Please choose:', reply_markup=reply_markup)

        def button(update, context):
            """Parses the CallbackQuery and updates the message text."""
            query = update.callback_query

            # CallbackQueries need to be answered, even if no notification to the user is needed
            # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
            query.answer()

            query.edit_message_text(text=f"Selected option: {query.data}")

        # Token
        updater = Updater(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM', use_context=True)
        dispatcher = updater.dispatcher


        # Debugger
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)


        # Start del bot

        # ** COMANDOS **
        start_handler = CommandHandler('registroCliente', registroCliente)
        start_handler2 = CommandHandler('registroUsuario', registroUsuario)
        start_handler3 = CommandHandler('test', test)
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(start_handler2)
        dispatcher.add_handler(start_handler3)
        dispatcher.add_handler(CallbackQueryHandler(button))
        updater.start_polling()



































# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Esta es la primera"
#                                                                     " vez que nos encontramos. Encantado de conocerte")




#context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Soy el asistente de la retificadora Sur Express. Me están construyendo, todavía soy un poco bobo")

#context.args[0]


#context.bot.send_message(chat_id=update.effective_chat.id, text=)



