
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
    if diaSemana == 5:
        if diaNotificacion.vienres:
            return True
        else:
            return False
    if diaSemana == 6:
        if diaNotificacion.sabado:
            return True
        else:
            return False
    if diaSemana == 7:
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
        eventos[evento.id] = 'no_notificar'
    return eventos

