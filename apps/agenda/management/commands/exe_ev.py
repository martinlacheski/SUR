from django.core.management.base import BaseCommand, CommandError
import telegram
from datetime import date, timedelta, datetime
from apps.agenda.models import *
from apps.agenda.logicaNotificacion import *

bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')


def scheduler_eventos():
    eventos = {}
    bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')
    dia_hoy = date.today()
    hora_actual = datetime.today()
    rango = datetime.today() - timedelta(minutes=10)
    dias_aviso = diasAvisoEvento.objects.get(diasAntelacion__gte=0)

    # Si hoy es dìa de notificación, empezamos. Sino, no hacemos nada
    if diaDeNotificacion(dia_hoy.weekday(), dias_aviso):
        tiposEventoSistema = tiposEvento.objects.filter(recordarSistema=True,
                                                        horarioRecordatorio__range=(rango.time(),
                                                                                    hora_actual.time()))
        data = eventosAgenda.objects.filter(tipoEvento__in=tiposEventoSistema)
        # Si no hay eventos en este rango horario, traigo los que ya se notificaron hoy
        if not data:
            print("no encontramos eventos en este rango de tiempo ~")

        # Si hay eventos, los analizo
        else:
            for evento in data:
                if evento.ultimaNotificacionTel == dia_hoy and (not evento.resuelto):
                    print("1")
                    pass
                else:
                    if evento.vencido or evento.resuelto:
                        print("2")
                        pass
                    else:
                        if evento.fechaNotificacion == dia_hoy:                                     # Se supone que nunca se va a ejecutar
                            bot.send_message(text="RECORDATORIO URGENTE", chat_id=630659758)
                            evento.ultimaNotificacionTel = dia_hoy
                            evento.cantNotifTelegram = evento.cantNotifTelegram + 1
                            evento.save()
                            print("3")
                        else:                                                                       # Si no vence hoy, vemos si es momento de notificarlo
                            if evento.cantNotifSistema < dias_aviso.diasAntelacion:
                                if restarDiasHabiles(evento.fechaNotificacion, dias_aviso.diasAntelacion) <= dia_hoy:
                                    bot.send_message(text="RECORDATORIO", chat_id=630659758)
                                    evento.ultimaNotificacionTel = date.today()
                                    evento.cantNotifTelegram = evento.cantNotifTelegram + 1
                                    evento.save()
                                    print("4")
                                else:
                                    print("5")
                                    pass


    else:
        print("no es dia de notificacion")


# Verificamos notificaciones urgentes
def notif_urgentes():
    dias_aviso = diasAvisoEvento.objects.get(diasAntelacion__gte=0)
    dia_hoy = date.today()
    hora_actual = datetime.today()

    if diaDeNotificacion(dia_hoy.weekday(), dias_aviso):
        eventos = eventosAgenda.objects.filter(fechaNotificacion=dia_hoy)

        for evento in eventos:
            if restarHora(evento.tipoEvento.horarioRecordatorio):
                # acá será chat_id del usuario que se haya registrado
                bot.send_message(text="EVENTO IMPORTANTE VENCIDO", chat_id=630659758)
            else:
                pass



class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler_eventos()
        #notif_urgentes()

