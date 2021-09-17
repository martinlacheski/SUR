from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler
import telegram
from datetime import datetime
import datetime
from apps.agenda.models import eventosAgenda

bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')


def msj_telegram(text):
    bot.send_message(text=text, chat_id=630659758)

def scheduler_eventos():

    # Especifico de APScheduler
    scheduler_eventos = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler_eventos.remove_all_jobs()


    # datos base para operaciones con fechas
    fecha_hoy = datetime.datetime.today()
    unaSem = datetime.timedelta(weeks=1)
    unDia = datetime.timedelta(days=1)
    unMes = datetime.timedelta(weeks=4)

    print("entramos al creador de eventos")
    eventosList = eventosAgenda.objects.all()
    for evento in eventosList:
        print(evento.repeticion)
        if(evento.repeticion == ''):
            msj = 'RECORDATORIO\n \nEvento de tipo: ' + evento.tipoEvento.nombre + '\n' \
                  + 'Descripción: ' + evento.descripcion + '\nVence en la fecha: ' \
                  + str(evento.fechaNotificacion.day) + '/' + str(evento.fechaNotificacion.month) \
                  + '/' + str(evento.fechaNotificacion.year)
            print("crea evento único")
            scheduler_eventos.add_job(msj_telegram, 'date',
                                      run_date=datetime.datetime(evento.fechaNotificacion.year,
                                                                 evento.fechaNotificacion.month,
                                                                 evento.fechaNotificacion.day,
                                                                 evento.tipoEvento.horarioRecordatorio.hour,
                                                                 evento.tipoEvento.horarioRecordatorio.minute,
                                                                 0),
                                      args=[msj]
                                      )

        if evento.repeticion == 'DIA':
            msj = 'RECORDATORIO\n \nEvento de tipo: ' + evento.tipoEvento.nombre + '\n' \
                  + 'Descripción: ' + evento.descripcion + '\nVence a las: ' \
                  + str(evento.tipoEvento.horarioRecordatorio.hour) + ' horas ' \
                  + 'y ' + str(evento.tipoEvento.horarioRecordatorio.minute) + 'minutos' \
                  + ' del día de hoy'
            print("crea evento diario")
            scheduler_eventos.add_job(msj_telegram, 'cron',
                                      hour=evento.tipoEvento.horarioRecordatorio.hour,
                                      minute=evento.tipoEvento.horarioRecordatorio.minute,
                                      second=0,
                                      args=[msj]
                                      )

        if evento.repeticion == 'SEM':
            # Se requiere una fun que convierta dia de la semana a español
            msj = 'RECORDATORIO\n \nEvento de tipo: ' + evento.tipoEvento.nombre + '\n' \
                  + 'Descripción: ' + evento.descripcion + '\nVence el dia: ' \
                  + 'resultado func' + 'de esta semana'
            print("creamos evento sem")
            scheduler_eventos.add_job(msj_telegram, 'cron',
                                      day_of_week=evento.fechaNotificacion.weekday(),
                                      hour=evento.tipoEvento.horarioRecordatorio.hour,
                                      minute=evento.tipoEvento.horarioRecordatorio.minute,
                                      second=0,
                                      args=[msj]
                                      )
        if evento.repeticion == 'MEN':

            msj = 'RECORDATORIO\n \nEvento de tipo: ' + evento.tipoEvento.nombre + '\n' \
                  + 'Descripción: ' + evento.descripcion + '\nVence el dia: ' \
                  + 'resultado func' + 'de esta semana (MES)'
            print("crea evento MENSUAL")
            scheduler_eventos.add_job(msj_telegram, 'cron',
                                      day=evento.fechaNotificacion.day,
                                      hour=evento.tipoEvento.horarioRecordatorio.hour,
                                      minute=evento.tipoEvento.horarioRecordatorio.minute,
                                      second=0,
                                      args=[msj]
                                      )
    scheduler_eventos.start()

    # if(evento.repeticion == 'DIA'):
    #     print("creamos evento")
    #     scheduler_eventos.add_job(msj_telegram, 'cron',
    #                               hour=evento.tipoEvento.horarioRecordatorio.hour,
    #                               minute=evento.tipoEvento.horarioRecordatorio.minute,
    #                               args=['holasasa'])


    # if (evento.repeticion == 'SEM'):
    #     while evento.fechaNotificacion <= fecha_hoy.date():
    #         evento.fechaNotificacion = evento.fechaNotificacion + unaSem
    #         if evento.fechaNotificacion == fecha_hoy.date():
    #             print("programamos evento")  # debería ser una funcion
    #
    # if(evento.repeticion == 'MES'):
    #     while evento.fechaNotificacion <= fecha_hoy.date():
    #         evento.fechaNotificacion = evento.fechaNotificacion + unMes
    #         if evento.fechaNotificacion == fecha_hoy.date():
    #             print("programamos evento")  # debería ser una funcion

    # # Crea un job para telegram
    # if(evento.tipoEvento.recordarTelegram):
    #     print("creamos recordatorio")
    #     scheduler_eventos.add_job(
    #         msj_telegram,
    #         'date',
    #         run_date=datetime(evento.fechaNotificacion.year,
    #                           evento.fechaNotificacion.month,
    #                           evento.fechaNotificacion.day,
    #                           evento.tipoEvento.horarioRecordatorio.hour,
    #                           evento.tipoEvento.horarioRecordatorio.minute,
    #                           0),
    #         args=['Recordatorio de evento {evento}. Vea que onda']
    #         )
    # # Crea un job para Recordar en el sistema
    # if(evento.tipoEvento.recordarSistema):
    #     print("acá hay que crear un nuevo job que tire notificaciones en el template")
    #
    # # Crea un job para recordar vía mail
    # if(evento.tipoEvento.recordarEmail):
    #     print("acá hay que crear un nuevo job que tire emails ")



# scheduler_eventos.add_job(
#     msj_telegram, 'cron',
#     second='*/5',
#     args=['holasasa'],
#     replace_existing=True
# )