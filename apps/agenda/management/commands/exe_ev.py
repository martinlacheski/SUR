from django.core.management.base import BaseCommand, CommandError
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
import datetime
import telegram


scheduler_eventos = BackgroundScheduler(timezone=settings.TIME_ZONE)

def notificar(evento):
    bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')
    bot.send_message(chat_id=630659758, text="holaaaaaaa")


def create_job(evento):
    scheduler_eventos.add_job(notificar, 'date',
                              run_date=datetime.datetime(evento.fechaNotificacion.year, evento.fechaNotificacion.month,
                                                         evento.fechaNotificacion.day,
                                                         evento.tipoEvento.horarioRecordatorio.hour,
                                                         evento.tipoEvento.horarioRecordatorio.minute, 0),
                              args=[evento])

class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler_eventos.start()





