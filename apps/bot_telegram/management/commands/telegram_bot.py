from django.core.management.base import BaseCommand, CommandError
import logging
from telegram.ext import Updater
import telegram
from telegram.ext import CommandHandler
from apps.usuarios.models import Usuarios
from apps.erp.models import Clientes


class Command(BaseCommand):



    def handle(self, *args, **options):
        bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')

        print("hola")
        # def registroUsuarios(update, context):
        #     if len(context.args) == 2:
        #         try:
        #             usuario = context.args[0]
        #             password = context.args[1]
        #             users = Usuarios.objects.all()
        #             user_ok = False
        #
        #             for user in users:
        #                 if context.args[0] == user.username and user.check_password(context.args[1]):
        #                     user_ok = True
        #                     print("Usuario registrado")
        #                     break
        #
        #             if user_ok:
        #                 update.message.reply_text("Usuario registrado con éxito")
        #             else:
        #                 update.message.reply_text("El usuario o la contraseña no coinciden")
        #         except Exception as e:
        #             print("Comando erroneo")
        #             update.message.reply_text("Comando erroneo, intente nuevamente.")
        #     else:
        #         print("Comando erroneo. Demasiados argumentos")
        #         update.message.reply_text("Comando erroneo. Cantidad de argumentos incorrecta. "\
        #                                   "\n\nIntente nuevamente escribiendo únicamente su usuario y su contraseña.")

        def registroCliente(update, context):
            print(len(context.args))
            print(str(update.message.from_user.username))
            if len(context.args) == 0:
                update.message.reply_text(text="Hola\! 👋 Este es el registro de clientes de SUR EXPRESS\.\n\n"
                                               "Para registrarte y recibir notificaciones ingresá el comando */registroCliente* "
                                               "y a continuación tu CUIL/CUIT sin guiones o comas\.\nPor ejemplo: \n\n"
                                               "``` /registroCliente 20346735739 ``` \n\n"
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

                        # Le avisamos al supervisor (chat_id tiene que ser de algun gerente o de TODOS los gerentes)
                        bot.send_message(text="Hola! 😌\nDisculpá las molestias, pero un cliente intentó registrarse y "
                                              "su CUIL/CUIT no estaba registrado.\n\n\n Sus datos son: \n\n"
                                              "CUIL/CUIT: " + cuil_cuit + "\n"
                                              "Usuario en Telegram: " + str(update.message.from_user.username) + "\n" +
                                              "Nombre en Telegram: " + str(update.message.from_user.first_name),
                                         chat_id=630659758)

                else:
                    update.message.reply_text("CUIL/CUIT ingresado contiene letras o no tiene una"
                                              " longitud de 11 caracteres")
            elif len(context.args) != 0 and len(context.args) != 1:
                    update.message.reply_text(text="No ingresaste bien el comando 😅\nRecordá que tiene que ser similar "
                                                   "a\n\n ``` /registroCliente 20346735739 ``` "
                                               ,parse_mode=telegram.ParseMode.MARKDOWN_V2)

            #if len(context.args) == 2:





        # Token
        updater = Updater(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM', use_context=True)
        dispatcher = updater.dispatcher


        # Debugger
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)


        # Start del bot

        # ** COMANDOS **
        start_handler = CommandHandler('registroCliente', registroCliente)
        # start_handler = CommandHandler('registroUsuario', registroUsuario)
        dispatcher.add_handler(start_handler)
        updater.start_polling()



































# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Esta es la primera"
#                                                                     " vez que nos encontramos. Encantado de conocerte")




#context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Soy el asistente de la retificadora Sur Express. Me están construyendo, todavía soy un poco bobo")

#context.args[0]


#context.bot.send_message(chat_id=update.effective_chat.id, text=)



