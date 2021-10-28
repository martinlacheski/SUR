from datetime import date, timedelta, datetime
from apps.agenda.models import *

def diaDeNotificacion(diaSemana, diaNotificacion):
    if diaSemana == 0 :
        if diaNotificacion.lunes:
            return True
        else:
            return False
    if diaSemana == 1:
        if diaNotificacion.martes:
            return True
        else:
            return False
    if diaSemana == 2:
        if diaNotificacion.miercoles:
            return True
        else:
            return False
    if diaSemana == 3:
        if diaNotificacion.jueves:
            return True
        else:
            return False
    if diaSemana == 4:
        if diaNotificacion.viernes:
            return True
        else:
            return False
    if diaSemana == 5:
        if diaNotificacion.sabado:
            return True
        else:
            return False
    if diaSemana == 6:
        if diaNotificacion.domingo:
            return True
        else:
            return False


def vencido(evento):
    if evento.vencido:
        return True
    else:
        return False


def eventosNotificadosHoy(eventosQuery):
    eventos = {}
    for evento in eventosQuery:
        if not evento.resuelto:
            if evento.ultimaVistaNotifiSist == date.today():
                eventos[evento.id] = ['no_notificar', str(evento.tipoEvento)]
            elif evento.ultimaVistaNotifiSist != date.today():
                if evento.vencido:
                    eventos[evento.id] = ['notificar_heavy', str(evento.tipoEvento)]
                else:
                    eventos[evento.id] = ['no_notificar_pendiente', str(evento.tipoEvento)]
    return eventos


# Resta días hábiles tomando en cuenta la fecha de notificación y los días de antelación
def restarDiasHabiles(Fnotif, diasAntelacion):
    fecha_resultado = Fnotif
    dias_hab_restados = 0
    while dias_hab_restados < diasAntelacion:
        fecha_resultado = fecha_resultado - timedelta(days=1)
        if fecha_resultado.weekday() in range(5):
            dias_hab_restados = dias_hab_restados + 1

    return fecha_resultado




#   Se usa para notificar una hora antes del vencimiento del evento.
#   Si devuelve True significa que la hora de notificación del evento - 1h
#   es igual a la hora actual, por ende, notificamos.

def restarHora(horaEvento):
    horaInt = horaEvento.hour
    horaInt = horaInt - 1
    resultado = horaEvento.replace(hour=horaInt)
    if resultado.hour == datetime.today().time().hour and resultado.minute == datetime.today().time().minute:
        return True
    else:
        return False


