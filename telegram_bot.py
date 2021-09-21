import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

updater = Updater(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM', use_context=True)
dispatcher = updater.dispatcher


def saludo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Soy el asistente de la retificadora Sur Express. Me están construyendo, todavía soy un poco bobo")

start_handler = CommandHandler('saludo', saludo)
dispatcher.add_handler(start_handler)
updater.start_polling()

           