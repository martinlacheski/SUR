from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
import telegram
from datetime import datetime
import datetime
from apps.agenda.models import eventosAgenda
from apps.usuarios.models import Usuarios
from apps.notif_channel.models import notificacionesGenerales
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.agenda.models import notificacionUsuarios, diasAvisoEvento
from apps.agenda.logicaNotificacion import restarDiasHabiles, diaDeNotificacion

bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')


# Especifico de APScheduler

def notificar(evento):
    print("me ejecuto")
    usersToNotify = notificacionUsuarios.objects.filter(tipoEvento=evento.tipoEvento)
    dias_aviso = diasAvisoEvento.objects.last()
    if diaDeNotificacion(datetime.date.today().weekday(), dias_aviso):
        for user in usersToNotify:
            if user.usuarioNotif.chatIdUsuario:
                if evento.tipoEvento.recordarTelegram:
                    msj = 'RECORDATORIO\n\n Hola! 👋 Recordá que programaste el siguiente evento: \n\n' \
                          ' \n📍 Evento de tipo: ' + evento.tipoEvento.nombre + '\n' \
                          + '📝 Descripción: ' + evento.descripcion + '\n🗓 Vence en la fecha: ' \
                          + str(evento.fechaNotificacion.day) + '/' + str(evento.fechaNotificacion.month) \
                          + '/' + str(evento.fechaNotificacion.year)
                    bot.send_message(text=msj, chat_id=user.usuarioNotif.chatIdUsuario)

            if evento.tipoEvento.recordarSistema:
                titulo = "Evento Pendiente - Tipo " + str(evento.tipoEvento)
                descripcion = "¡RECUERDE!\n\n Evento de tipo " + str(evento.tipoEvento) + " programado para el día " + \
                              evento.fechaNotificacion.strftime('%d-%m-%Y') + " con " \
                              "descripción: '" + str(evento.descripcion) + "'."
                n = notificacionesGenerales()
                n.fechaNotificacion = datetime.datetime.today()
                n.estado = 'pendiente'
                n.titulo = titulo
                n.descripcion = descripcion
                n.enviadoAUser = user.usuarioNotif
                n.save()
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)('telegram_group',
                                                        {"type": "receive",
                                                         "titulo": titulo,
                                                         "id_notif": str(n.id)})

def notificar_generic(evento):
    return "hola"

def scheduler_evento(evento):
    scheduler_eventos = BackgroundScheduler(timezone=settings.TIME_ZONE)
    print("entramos al creador de eventos")
    if evento.repeticion == '':
        print("crea evento único")
        d = restarDiasHabiles(evento.fechaNotificacion, diasAvisoEvento.objects.last().diasAntelacion)
        print(d)
        print(type(d))
        start_date = datetime.datetime(year=d.year,
                              month=d.month,
                              day=d.day,
                              hour=evento.tipoEvento.horarioRecordatorio.hour,
                              minute=evento.tipoEvento.horarioRecordatorio.minute)
        print(start_date)
        end_date = datetime.datetime(year=evento.fechaNotificacion.year,
                            month=evento.fechaNotificacion.month,
                            day=evento.fechaNotificacion.day,
                            hour=evento.tipoEvento.horarioRecordatorio.hour,
                            minute=evento.tipoEvento.horarioRecordatorio.minute)
        print(end_date)
        scheduler_eventos.add_job(notificar, 'interval', minutes=1, args=[evento])
    scheduler_eventos.start()
    # if evento.repeticion == '':
    #     print("crea evento único")
    #     scheduler_eventos.add_job(notificar_generic, 'cron',
    #                               hour=evento.tipoEvento.horarioRecordatorio.hour,
    #                               minute=evento.tipoEvento.horarioRecordatorio.minute,
    #                               second=0,
    #                               args=[evento]
    #                               )
    #
    # if evento.repeticion == 'weekly':
    #     print("creamos evento sem")
    #     scheduler_eventos.add_job(notificar, 'cron',
    #                               day_of_week=evento.fechaNotificacion.weekday(),
    #                               hour=evento.tipoEvento.horarioRecordatorio.hour,
    #                               minute=evento.tipoEvento.horarioRecordatorio.minute,
    #                               second=0,
    #                               args=[evento]
    #                               )
    #
    # if evento.repeticion == 'monthly':
    #     print("crea evento MENSUAL")
    #     scheduler_eventos.add_job(notificar, 'cron',
    #                               day=evento.fechaNotificacion.day,
    #                               hour=evento.tipoEvento.horarioRecordatorio.hour,
    #                               minute=evento.tipoEvento.horarioRecordatorio.minute,
    #                               second=0,
    #                               args=[evento]
    #                               )
    #
    # scheduler_eventos.start()

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