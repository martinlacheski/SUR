from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
import telegram
from datetime import datetime
from apps.agenda.models import eventosAgenda

bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')

def msj_telegram(msj):
    bot.send_message(text=msj, chat_id=630659758)

def scheduler_eventos():
    scheduler_eventos = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler_eventos.remove_all_jobs()

    print("entramos al creador de eventos")
    eventosList = eventosAgenda.objects.all()
    for evento in eventosList:

        # Crea un job para telegram
        if(evento.tipoEvento.recordarTelegram):
            scheduler_eventos.add_job(
                msj_telegram,
                'date',
                run_date=datetime(evento.fechaNotificacion.year,
                                  evento.fechaNotificacion.month,
                                  evento.fechaNotificacion.day,
                                  evento.tipoEvento.horarioRecordatorio.hour,
                                  evento.tipoEvento.horarioRecordatorio.minute,
                                  0),
                args=['Recordatorio de evento {evento}. Vea que onda']
                )

        # Crea un job para Recordar en el sistema
        if(evento.tipoEvento.recordarSistema):
            print("acá hay que crear un nuevo job que tire notificaciones en el template")

        # Crea un job para recordar vía mail
        if(evento.tipoEvento.recordarEmail):
            print("acá hay que crear un nuevo job que tire emails ")

    scheduler_eventos.start()
    # for evento in eventosList:
    #     print("este es evento ", evento.id)
    #     print(evento.tipoEvento.recordarTelegram)
    #     print()