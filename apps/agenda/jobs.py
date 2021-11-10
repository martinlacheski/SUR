from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
import telegram
from datetime import datetime, timedelta
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
    usersToNotify = notificacionUsuarios.objects.filter(tipoEvento=evento.tipoEvento)
    dias_aviso = diasAvisoEvento.objects.last()
    if diaDeNotificacion(datetime.date.today().weekday(), dias_aviso):
        for user in usersToNotify:
            if user.usuarioNotif.chatIdUsuario:
                if evento.tipoEvento.recordarTelegram and (not evento.vencido or not evento.resuelto):
                    if evento.fechaNotificacion - timedelta(days=1) == datetime.date.today():
                        msj = 'RECORDATORIO URGENTE 🚨\n\n Hola! 👋 Recordá que programaste el siguiente evento el ' \
                              'cual vence MAÑANA: \n\n' \
                              ' \n📍 Evento de tipo: ' + evento.tipoEvento.nombre + '\n' + '📝 Descripción: ' +\
                              evento.descripcion + '\n🗓 Vence en la fecha: ' +\
                              str(evento.fechaNotificacion.strftime('%d-%m-%Y'))
                    else:
                        msj = 'RECORDATORIO\n\n Hola! 👋 Recordá que programaste el siguiente evento: \n\n' \
                              ' \n📍 Evento de tipo: ' + evento.tipoEvento.nombre + '\n' \
                              + '📝 Descripción: ' + evento.descripcion + '\n🗓 Vence en la fecha: ' \
                              +  str(evento.fechaNotificacion.strftime('%d-%m-%Y'))
                    bot.send_message(text=msj, chat_id=user.usuarioNotif.chatIdUsuario)

            if evento.tipoEvento.recordarSistema and (not evento.vencido or not evento.resuelto):
                n = notificacionesGenerales()
                if evento.fechaNotificacion - timedelta(days=1) == datetime.date.today():
                    print("hola")
                    n.estado = 'urgente'
                    titulo = "Evento URGENTE - Tipo " + str(evento.tipoEvento)
                    descripcion = "¡RECUERDE!\n\n Evento de tipo " + str(evento.tipoEvento) + " programado para el día " + \
                                  evento.fechaNotificacion.strftime('%d-%m-%Y') + " (MAÑANA) con " \
                                  "descripción: '" + str(evento.descripcion) + "'."
                else:
                    n.estado = 'pendiente'
                    titulo = "Evento Pendiente - Tipo " + str(evento.tipoEvento)
                    descripcion = "¡RECUERDE!\n\n Evento de tipo " + str(evento.tipoEvento) + \
                                  " programado para el día " + evento.fechaNotificacion.strftime('%d-%m-%Y') + \
                                  " con descripción: '" + str(evento.descripcion) + "'."
                n.fechaNotificacion = datetime.datetime.today()

                n.titulo = titulo
                n.descripcion = descripcion
                n.enviadoAUser = user.usuarioNotif
                n.save()
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)('telegram_group',
                                                        {"type": "receive",
                                                         "titulo": titulo,
                                                         "id_notif": str(n.id)})
            if evento.fechaNotificacion == datetime.date().today():
                evento.vencido = True
                evento.save()

def notificar_generic(evento):
    usersToNotify = notificacionUsuarios.objects.filter(tipoEvento=evento.tipoEvento)
    dias_aviso = diasAvisoEvento.objects.last()
    if diaDeNotificacion(datetime.date.today().weekday(), dias_aviso):
        for user in usersToNotify:
            if user.usuarioNotif.chatIdUsuario:
                if evento.tipoEvento.recordarTelegram:
                    msj = 'RECORDATORIO\n\n Hola! 👋 Recordá que programaste el siguiente evento: \n\n' \
                          ' \n📍 Evento de tipo: ' + evento.tipoEvento.nombre + '\n' + '📝 Descripción: ' +\
                          evento.descripcion + '\n🗓 Vence en la fecha: ' +\
                          str(evento.fechaNotificacion.strftime('%d-%m-%Y'))
                    bot.send_message(text=msj, chat_id=user.usuarioNotif.chatIdUsuario)

                if evento.tipoEvento.recordarSistema:
                    titulo = "Evento Pendiente - Tipo " + str(evento.tipoEvento)
                    descripcion = "¡RECUERDE!\n\n Evento de tipo " + str(evento.tipoEvento) + \
                                  " programado para el día " + evento.fechaNotificacion.strftime('%d-%m-%Y') \
                                  + " con descripción: '" + str(evento.descripcion) + "'."
                    n = notificacionesGenerales()
                    n.estado = 'pendiente'
                    n.fechaNotificacion = datetime.datetime.today()
                    n.titulo = titulo
                    n.descripcion = descripcion
                    n.enviadoAUser = user.usuarioNotif
                    n.save()
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)('telegram_group',
                                                            {"type": "receive",
                                                             "titulo": titulo,
                                                             "id_notif": str(n.id)})


def scheduler_evento(evento):
    scheduler_eventos = BackgroundScheduler(timezone=settings.TIME_ZONE)
    start_date = datetime.datetime(year=evento.fechaNotificacion.year,
                                   month=evento.fechaNotificacion.month,
                                   day=evento.fechaNotificacion.day,
                                   hour=evento.tipoEvento.horarioRecordatorio.hour,
                                   minute=evento.tipoEvento.horarioRecordatorio.minute)
    end_date = datetime.datetime(year=evento.fechaNotificacion.year,
                                 month=evento.fechaNotificacion.month,
                                 day=evento.fechaNotificacion.day,
                                 hour=evento.tipoEvento.horarioRecordatorio.hour,
                                 minute=evento.tipoEvento.horarioRecordatorio.minute)
    if evento.repeticion == '':
        print("crea evento único")
        d = restarDiasHabiles(evento.fechaNotificacion, diasAvisoEvento.objects.last().diasAntelacion)
        start_date_unic = datetime.datetime(year=d.year, month=d.month, day=d.day,
                                       hour=evento.tipoEvento.horarioRecordatorio.hour,
                                       minute=evento.tipoEvento.horarioRecordatorio.minute)
        scheduler_eventos.add_job(notificar, 'interval', days=1,
                                  start_date=start_date_unic,
                                  end_date=end_date,
                                  args=[evento])
    if evento.repeticion == 'daily':
        print("crea evento diario")
        scheduler_eventos.add_job(notificar_generic, 'interval', days=1,
                                  start_date=start_date,
                                  end_date=end_date,
                                  args=[evento])

    if evento.repeticion == 'weekly':
        print("creamos evento sem")
        scheduler_eventos.add_job(notificar_generic, 'interval', weeks=1,
                                  start_date=start_date,
                                  end_date=end_date,
                                  args=[evento])

    if evento.repeticion == 'monthly':
        print("crea evento MENSUAL")
        scheduler_eventos.add_job(notificar_generic, 'interval', weeks=4,
                                  start_date=start_date,
                                  end_date=end_date,
                                  args=[evento])
    scheduler_eventos.start()