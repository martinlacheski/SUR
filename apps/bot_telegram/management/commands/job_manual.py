from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
import datetime
import random
import telegram
from apscheduler.schedulers.background import BlockingScheduler
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from apps.bot_telegram.logicaBot import porcentajeTrabajo, notificarSistema
from apps.bot_telegram.models import seguimientoTrabajos
from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from apps.usuarios.models import Usuarios

bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')

class Command(BaseCommand):
    def handle(self, *args, **options):
        t = seguimientoTrabajos.objects.all().last().trabajo
        segTrab = seguimientoTrabajos.objects.get(trabajo=t)
        # Si el usuario no respondió o si respondió "Postergar", entra
        if not segTrab.respuestaUser or segTrab.respuestaUser == 'Postergar':
            print("no tiene respuesta o puso postergar")
            # Si se notificó más de 3 veces, se reasigna. Se notifica al usuario que "perdió" el trabajo y tmb a administraición
            if segTrab.cantVecesNotif_dia >= 3:
                reasignacionTrabajo(t, segTrab)
                print("se reasignó el trabajo")
                # Se le notifica a quien perdió el trabajo
                if segTrab.inicialUserAsig.chatIdUsuario:
                    bot.send_message(chat_id=segTrab.inicialUserAsig.chatIdUsuario,
                                     text="🔴 Por falta de respuesta he reasignado tu trabajo Nro° " + str(t.id) +
                                          ". El mismo ya no será tu responsabilidad.")
                titulo = "Cambio de asignación de Trabajo"
                descripcion = "El trabajo Nro° " + str(t.id) + " originalmente responsabilidad del usuario " + \
                              str(segTrab.inicialUserAsig.username) + ", fué re-asignado al usuario  " + \
                              str(segTrab.ultUserAsig.username) + "."
                # Se notifica por sistema
                notificarSistema(titulo, descripcion)

                # se notifica al nuevo responsable del trabajo
                if segTrab.ultUserAsig.chatIdUsuario:
                    bot.send_message(chat_id=segTrab.ultUserAsig.chatIdUsuario,
                                     text="⚠ AVISO ⚠ \nTe he asignado el trabajo  Nro° " + str(t.id) + ".")
            else:
                print("Se notificó " + str(segTrab.cantVecesNotif_dia) + " veces")
                # Usamos el try en caso de que se quiera evaluar un usuario NONE (trabajo express)
                try:
                    # Si el usuario tiene chatId y aúno no le avisamos 3 veces, armamos msj con botones y enviamos.
                    if t.usuarioAsignado.chatIdUsuario:
                        bot.send_message(chat_id=t.usuarioAsignado.chatIdUsuario, text=mensaje(t))
                        faltan_repuestos = {'trabajo': str(t.id), 'respuesta': "Faltan repuestos"}
                        postergar = {'trabajo': str(t.id), 'respuesta': "Postergar"}
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
                        segTrab.fechaEnvio = timezone.now().today()
                        segTrab.save()
                    # Si el usuario no tiene chatID, informamos mediante sistema.
                    else:
                        if segTrab.notif_por_sist < 1:  # if para que esto se notifique solamente UNA VEZ por sistema
                            titulo = "Aviso de trabajo pendiente fallido"
                            descripcion = "No se pudo notificar al usuario " + str(
                                t.usuarioAsignado.username) + " que" \
                                                              " su trabajo Nroª " + str(
                                t.id) + " se encuentra atrasado debido a que el mismo" \
                                        " no está registrado con el BOT."
                            notificarSistema(titulo, descripcion)
                            segTrab.notif_por_sist += 1
                            segTrab.save()
                except AttributeError:
                    titulo = "Trabajo atrasado sin usuario asignado"
                    descripcion = "El trabajo Nro° " + str(t.id) + " se encuentra atrasado " \
                                                                   "según su prioridad y no tiene un usuario asignado."
                    notificarSistema(titulo, descripcion)



# Aplica los 3 diferentes criterios donde cada criterio tiene en cuenta el anterior.
def reasignacionTrabajo(trabajo, segTrabajo):
    empAEvaluar = eleccionUsuarios(trabajo.usuarioAsignado)

    # Si unicamente existe un usuario aparte del que ya tiene asignado el trabajo, se lo damos a ese.
    if len(empAEvaluar) == 1:
        nuevoUserAsig = Usuarios.objects.get(pk=empAEvaluar[0]['usuarioAsignado'])
        segTrabajo.ultUserAsig = nuevoUserAsig
        segTrabajo.save()
        trabajo.usuarioAsignado = Usuarios.objects.get(pk=nuevoUserAsig.id)
        trabajo.save()

    # Si no hay emps ademas del que ya está encargado, reportamos
    elif len(empAEvaluar) == 0:
        titulo = "Trabajo atrasado sin usuario al cual asignar."
        descripcion = "El trabajo Nro° " + str(trabajo.id) + " se encuentra atrasado" \
                                                             "según su prioridad y no hay usuario a quien re-asignarselo."
        notificarSistema(titulo, descripcion)

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
                    'avance': avanceXEmp,
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
                listEmpSel = []
                empSeleccionado = random.choice(empSeleccionados)
                listEmpSel.append(empSeleccionado)
                eleccionUnitaria(listEmpSel, segTrabajo)



    """ Realiza una sumatoria del avance total de todos los trabajos de cada empleado.
        No tiene en cuenta trabajos finalizados, cancelados o entregados. """
def avanceTotalizado(empleado):
    estados = EstadoParametros.objects.last()
    estados_filter = [estados.estadoEspecial.id, estados.estadoInicial.id, estados.estadoPlanificado.id]
    trabajosEmp = Trabajos.objects.filter(usuarioAsignado=empleado['usuarioAsignado'], estadoTrabajo__in=estados_filter)
    avance = 0
    for t in trabajosEmp:
        avance += float(porcentajeTrabajo(t))
    return avance


# Encargada de efectivamente realizar la re-asiganción.
def eleccionUnitaria(empSeleccionados, segTrabajo):
    if len(empSeleccionados) == 1:
        nuevoUserAsig = Usuarios.objects.get(pk=empSeleccionados[0]['usuarioAsignado'])
        segTrabajo.ultUserAsig = nuevoUserAsig
        segTrabajo.save()
        trab = Trabajos.objects.get(pk=segTrabajo.trabajo.id)
        trab.usuarioAsignado = Usuarios.objects.get(pk=nuevoUserAsig.id)
        trab.save()
        print()
        return True
    else:
        return False


# Arma titulo y mensaje de notificación por Sistema. Llama a la función original de logicaBot
def msjNotificarSistema(nuevoUser, trabajo, segTrabajo):
    oldUser = Usuarios.objects.get(pk=segTrabajo.inicialUserAsig.id)
    titulo = "Cambio de asignación de Trabajo"
    descripcion = "El trabajo Nro° " + str(trabajo.id) + " originalmente responsabilidad del usuario " \
                  + str(oldUser.username) + ", fué re-asignado al usuario  " + str(nuevoUser.username) + "."
    notificarSistema(titulo, descripcion)


    """ Obtiene todos los usuarios que pueden realizar trabajos y luego vé
        cuantos trabajos tiene asignado cada uno.
        Devuelve una lista de diccionarios que contiene c/u
        un usuario y cuanto trab tiene asignados. """
def eleccionUsuarios(userTrabajo):
    empsAEvaluar = []
    # Se toman todos los usuarios excepto el responsable inicial del trabajo
    users = Usuarios.objects.filter(realizaTrabajos=True).exclude(pk=userTrabajo.id)
    estados = EstadoParametros.objects.last()
    estados_filter = [estados.estadoEspecial.id, estados.estadoInicial.id, estados.estadoPlanificado.id]
    for u in users:
        t_asig = Trabajos.objects.filter(usuarioAsignado=u, estadoTrabajo__in=estados_filter)
        dict_users = {'usuarioAsignado': str(u.id), 'count': len(t_asig), }
        empsAEvaluar.append(dict_users)
    print(dict_users)
    return empsAEvaluar



def mensaje(t):
    mensaje = "Hola! 👋 Te informo que el trabajo Nro°" + str(t.id) + "\n\n" + \
              "Marca: " + str(t.modelo.marca.nombre) + "\n" + "Modelo: " + str(t.modelo.nombre) + "\n\n" + \
              "No está finalizado según la prioridad establecida.\n"
    return mensaje