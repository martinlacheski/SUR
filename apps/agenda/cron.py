import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

def cron_prueba():
    bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')
    bot.send_message(text='Prueba', chat_id=630659758)