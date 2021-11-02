import datetime
import random
import telegram
from apscheduler.schedulers.background import BlockingScheduler
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from apps.bot_telegram.logicaBot import porcentajeTrabajo, notificarSistema
from apps.bot_telegram.models import seguimientoTrabajos
from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos, DetalleServiciosTrabajo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.db.models import Count
from apps.usuarios.models import Usuarios
from apps.bot_telegram.logicaBot import porcentajeTrabajo


bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')

class Command(BaseCommand):
    def handle(self, *args, **options):

        # APS
        scheduler_eventos = BlockingScheduler(timezone=settings.TIME_ZONE)
        start_date = datetime.datetime.today()
        end_date = datetime.datetime.today() + datetime.timedelta(hours=3)

        # Buscamos trabajos que no estén en ninguno de estos estados.
        estados = EstadoParametros.objects.last()
        estados_excluidos = [estados.estadoFinalizado.id,
                             estados.estadoEntregado.id,
                             estados.estadoCancelado.id]
        trabajos = Trabajos.objects.exclude(estadoTrabajo__in=estados_excluidos)

        # Armamos una lista de los trabajos a supervisar
        trabajosASupervisar = []
        for t in trabajos:
            # avance = porcentajeTrabajo(t)
            cant_dias_en_proceso = datetime.date.today() - t.fechaEntrada
            # Si la cantidad de días desde que el trabajo está en la empresa es mayor a su plazo aproximado, hacemos cosas
            if cant_dias_en_proceso.days > t.prioridad.plazoPrioridad:
                try:
                    # Si ya existe un seguimiento para el trabajo en cuestión, ponemos su cant notif diaria a 0
                    segTrab = seguimientoTrabajos.objects.get(trabajo=t)
                    segTrab.cantVecesNotif_dia = 0
                except ObjectDoesNotExist:
                    # Si no existe, creamos un seguimiento
                    segTrab = seguimientoTrabajos()
                    segTrab.trabajo = t
                    segTrab.inicialUserAsig = t.usuarioAsignado
                    # segTrab.ultPorcentajeAvance = float(avance)
                    segTrab.cantVecesNotif_dia = 0
                segTrab.save()
                trabajosASupervisar.append(t)
        if trabajosASupervisar:
            scheduler_eventos.add_job(self.job, 'interval', seconds=100, args=[trabajosASupervisar]) # Se tiene que setear para que se ejecute 4 veces
            scheduler_eventos.start()

    def job(self, t_supervisar):
        for t in t_supervisar:
            segTrab = seguimientoTrabajos.objects.get(trabajo=t)
            # Envía notificaciones siempre y cuando no haya respuesta.
            if not segTrab.respuestaUser:
                if segTrab.cantVecesNotif_dia >= 3:
                    reasignacionTrabajo(t)
                else:
                    try:
                        if t.usuarioAsignado.chatIdUsuario:
                            # Arma mensaje
                            bot.send_message(chat_id=t.usuarioAsignado.chatIdUsuario, text=mensaje(t))
                            # Callback data
                            faltan_repuestos = {'trabajo': str(t.id), 'respuesta': "Faltan repuestos"}
                            postergar = {'trabajo': str(t.id), 'respuesta': "Postergar"}
                            # Arma botones y los envia
                            keyboard = [
                                        [InlineKeyboardButton("🛠 Faltan repuestos", callback_data=str(faltan_repuestos))],
                                        [InlineKeyboardButton("🕙 Postergar", callback_data=str(postergar))],
                                       ]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            bot.send_message(chat_id=t.usuarioAsignado.chatIdUsuario,
                                             text="Elegí una opción: \n",
                                             reply_markup=reply_markup)
                            # Actualiza seguimiento
                            segTrab.cantVecesNotif_dia += 1
                            segTrab.fechaEnvio= datetime.datetime.today()
                            segTrab.save()
                    except AttributeError:
                        print("TO-DO: acá hay que avisar que un trabajo express sin usuario asignado está estancando")



def mensaje(t):
    mensaje = "Hola! 👋 Te informo que el trabajo Nro°" + str(t.id) + "\n\n" +\
    "Marca: " + str(t.modelo.marca.nombre) + "\n" + "Modelo: " + str(t.modelo.nombre) + "\n\n" +\
    "No está finalizado según la prioridad establecida.\n"
    return mensaje

#                                   __ CRITERIOS__

#               PRIMER CRITERIO:    Trabajador con menos trabajos asignados.
#               SEGUNDO CRITERIO:   Trabajador con mayor avance en totalidad de trabajos.
#                                   Se asume que todos tienen la misma cantidad de trabajos
#                                   debido al primer criterio.
#               TERCER CRITERIO:    De manera aleatoria, habiendose evaluado los criterios 1 y 2,
#                                   se toma un trabajador de manera aleatoria

# Función principal. Aplica los 3 diferentes criterios donde cada criterio tiene en cuenta el anterior.
def reasignacionTrabajo(trabajo):
    segTrabajo = seguimientoTrabajos.objects.get(trabajo=trabajo)
    estados = EstadoParametros.objects.last()
    estados_filter = [estados.estadoEspecial.id,
                      estados.estadoInicial.id,
                      estados.estadoPlanificado.id]
    empAEvaluar = Trabajos.objects.exclude(usuarioAsignado=trabajo.usuarioAsignado).\
                                   values('usuarioAsignado').annotate(count=Count('id')). \
                                   order_by().\
                                   filter(estadoTrabajo__in=estados_filter)

    # Si unicamente existe un usuario aparte del que ya tiene asignado el trabajo, se lo damos a ese.
    if len(empAEvaluar) == 1:
        nuevoUserAsig = Usuarios.objects.get(pk=empAEvaluar[0]['usuarioAsignado'])
        segTrabajo.ultUserAsig = nuevoUserAsig
        segTrabajo.save()
        trabajo.usuarioAsignado = Usuarios.objects.get(pk=nuevoUserAsig)
        trabajo.save()


    # Si no hay emps ademas del que ya está encargado, reportamos
    elif len(empAEvaluar) == 0:
        print("Notificar a administración que el trabajo está retardado y no hay usuario a quien asignar")

    # Si hay candidatos, evaluamos
    elif len(empAEvaluar) > 1:                                          # Primer criterio
        empSeleccionados = []
        auxEmp = empAEvaluar[0]
        for emp in empAEvaluar:
            if emp['count'] < auxEmp['count']:
                auxEmp = emp
        for emp in empAEvaluar:
            if emp['count'] == auxEmp['count']:
                empSeleccionados.append(emp)

        if not eleccionUnitaria(empSeleccionados, segTrabajo):          # Segundo criterio
            listadoAvances = []
            for emp in empSeleccionados:
                avanceXEmp = avanceTotalizado(emp)
                auxAvances = {
                    'usuarioAsignado': emp['usuarioAsignado'],
                    'avance' : avanceXEmp,
                }
                listadoAvances.append(auxAvances)
            empSeleccionados = []
            mayorAvance = listadoAvances[0]
            for emp in listadoAvances:
                if emp['avance'] > mayorAvance['avance']:
                    mayorAvance = emp
            for emp in listadoAvances:
                if emp['avance'] == mayorAvance['avance']:
                    empSeleccionados.append(emp)

            if not eleccionUnitaria(empSeleccionados, segTrabajo):      # Tercer criterio
                empRandom = random.choice(empSeleccionados)
                if not empRandom['usuarioAsignado']:
                    reasignacionTrabajo(trabajo)
                else:
                    eleccionUnitaria(empSeleccionados, segTrabajo)

# Realiza una sumatoria del avance total de todos los trabajos de cada empleado.
# No tiene en cuenta trabajos finalizados, cancelados o entregados.
def avanceTotalizado(empleado):
    estados = EstadoParametros.objects.last()
    estados_filter = [estados.estadoEspecial.id, estados.estadoInicial.id, estados.estadoPlanificado.id]
    trabajosEmp = Trabajos.objects.filter(usuarioAsignado=empleado['usuarioAsignado'], estadoTrabajo__in=estados_filter)
    avance = 0
    for t in trabajosEmp:
        avance += float(porcentajeTrabajo(t))
    return avance

# Encargada de efectivamente realizar la re-asiganción y de llamar al notificador.
def eleccionUnitaria(empSeleccionados, segTrabajo):
    if len(empSeleccionados) == 1:
        if not (empSeleccionados[0]['usuarioAsignado']):
            print("usuario NONE")
        else:
            nuevoUserAsig = Usuarios.objects.get(pk=empSeleccionados[0]['usuarioAsignado'])
            segTrabajo.ultUserAsig = nuevoUserAsig
            segTrabajo.save()
            trab = Trabajos.objects.get(pk=segTrabajo.trabajo.id)
            trab.usuarioAsignado = Usuarios.objects.get(pk=nuevoUserAsig)
            trab.save()
            msjNotificarSistema(nuevoUserAsig, trab, segTrabajo)
        return True
    else:
        return False

# Arma titulo y mensaje de notificación por Sistema. Llama a la función original de logicaBot
def msjNotificarSistema(nuevoUser, trabajo, segTrabajo):
    oldUser = Usuarios.objects.get(pk=segTrabajo.inicialUserAsig)
    titulo = "Cambio de asignación de Trabajo"
    descripcion = "El trabajo Nro° " + str(trabajo.id) + " originalmente responsabilidad del usuario " \
                  + str(oldUser.username) + ", fué re-asignado al usuario  " + str(nuevoUser.username) + "."
    notificarSistema(titulo, descripcion)