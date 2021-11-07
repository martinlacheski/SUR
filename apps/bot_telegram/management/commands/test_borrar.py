from django.utils import timezone
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
from apps.usuarios.models import TiposUsuarios

bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')

class Command(BaseCommand):
    def handle(self, *args, **options):
        estados = EstadoParametros.objects.last()
        estados_excluidos = [estados.estadoFinalizado.id, estados.estadoEntregado.id, estados.estadoCancelado.id]
        trabajos = Trabajos.objects.exclude(estadoTrabajo__in=estados_excluidos)

        # Armamos una lista de los trabajos a supervisar
        trabajosASupervisar = []
        for t in trabajos:
            cant_dias_en_proceso = timezone.now().date() - t.fechaEntrada
            # Si la cantidad de días desde que el trabajo está en la empresa es mayor a su plazo aproximado, hacemos cosas
            if cant_dias_en_proceso.days > t.prioridad.plazoPrioridad:
                try:
                    # Si ya existe un seguimiento para el trabajo en cuestión, ponemos su cant notif diaria a 0
                    segTrab = seguimientoTrabajos.objects.get(trabajo=t)
                    segTrab.cantVecesNotif_dia = 0
                    segTrab.cantVecesNotif_dia = 0
                    segTrab.respuestaUser = ""
                    segTrab.notif_por_sist = 0
                except ObjectDoesNotExist:
                    # Si no existe, creamos un seguimiento
                    segTrab = seguimientoTrabajos()
                    segTrab.trabajo = t
                    segTrab.inicialUserAsig = t.usuarioAsignado
                    segTrab.cantVecesNotif_dia = 0
                    segTrab.notif_por_sist = 0
                #segTrab.save()
                trabajosASupervisar.append(t)
        # Si hay trabajos para supervisar, creamos un job.
        if trabajosASupervisar:
            job(trabajosASupervisar)
            #print(trabajosASupervisar)

def job(t_supervisar):
    # Por cada trabajo en la lista de trabajos que están fuera de periodo
    for t in t_supervisar:
        print("\n\nANALIZANDO TRABAJO: " + str(t))
        segTrab = seguimientoTrabajos.objects.get(trabajo=t)
        # Envía notificaciones siempre y cuando no haya respuesta o la respuesta haya sido 'Postergar'
        if not segTrab.respuestaUser or segTrab.respuestaUser == 'Postergar':
            print("Tiene respuesta: " + str(segTrab.respuestaUser))
            # Si se notificó más de 3 veces, se reasigna. Se notifica al usuario que "perdió" el trabajo y tmb a administraición
            if segTrab.cantVecesNotif_dia >= 3:
                print("[dentro de if] Se notificó " + str(segTrab.cantVecesNotif_dia) + " veces")
                if t.usuarioAsignado.chatIdUsuario:
                    bot.send_message(chat_id=t.usuarioAsignado.chatIdUsuario,
                                     text="🔴 Por falta de respuesta he reasignado tu trabajo Nro° " + str(t.id) + ".")
                reasignacionTrabajo(t, segTrab)
                titulo = "Cambio de asignación de Trabajo"
                descripcion = "El trabajo Nro° " + str(t.id) + " originalmente responsabilidad del usuario " +\
                              str(segTrab.inicialUserAsig.username) + ", fué re-asignado al usuario  " +\
                              str(segTrab.ultUserAsig.username) + "."
                notificarSistema(titulo, descripcion)
            else:
                print("[fuera de if] Se notificó " + str(segTrab.cantVecesNotif_dia) + " veces")
                # Usamos el try en caso de que se quiera evaluar un usuario NONE (trabajo express)
                try:
                    print("El usuario asignado a este trabajo es: " + str(t.usuarioAsignado.username))
                except AttributeError:
                    print("El usuario asignado a este trabajo es un NONE")
                try:
                    # Si el usuario tiene chatId, armamos msj con botones y enviamos.
                    if t.usuarioAsignado.chatIdUsuario:
                        print("Dicho usuario tiene chatID. Vamos a notificar")
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
                        print("Dicho usuario no tiene chatID. Notificamos a administración")
                        if segTrab.notif_por_sist < 1:
                            titulo = "Aviso de trabajo pendiente fallido"
                            descripcion = "No se pudo notificar al usuario " + str(t.usuarioAsignado.username) + " que" \
                                          " su trabajo Nroª " + str(t.id) + " se encuentra atrasado debido a que el mismo" \
                                          " no está registrado con el BOT."
                            notificarSistema(titulo, descripcion)
                            segTrab.notif_por_sist += 1
                            segTrab.save()
                        else:
                            print("Ya notificamos 1 vez por sistema. No vamos a notificar nuevamente")
                except AttributeError:
                    print("Como era un usuario NONE, notificamos a administración")
                    titulo = "Trabajo atrasado sin usuario asignado"
                    descripcion = "El trabajo Nro° " + str(t.id) + " se encuentra atrasado " \
                                  "según su prioridad y no tiene un usuario asignado."
                    notificarSistema(titulo, descripcion)
        # Si la respuesta fué que faltan repuestos, se notifica a la administración (esto se encuetnra en telegram_bot.py)



def mensaje(t):
    mensaje = "Hola! 👋 Te informo que el trabajo Nro°" + str(t.id) + "\n\n" + \
              "Marca: " + str(t.modelo.marca.nombre) + "\n" + "Modelo: " + str(t.modelo.nombre) + "\n\n" + \
              "No está finalizado según la prioridad establecida.\n"
    return mensaje

#                                   __ CRITERIOS__

#               PRIMER CRITERIO:    Trabajador con menos trabajos asignados.
#               SEGUNDO CRITERIO:   Trabajador con mayor avance en totalidad de trabajos.
#                                   Se asume que todos tienen la misma cantidad de trabajos
#                                   debido al primer criterio.
#               TERCER CRITERIO:    De manera aleatoria, habiendose evaluado los criterios 1 y 2,
#                                   se toma un trabajador de manera aleatoria


# Aplica los 3 diferentes criterios donde cada criterio tiene en cuenta el anterior.
def reasignacionTrabajo(trabajo, segTrabajo):

    # Elección de usuarios
    empAEvaluar = eleccionUsuarios(trabajo.usuarioAsignado)
    # Si unicamente existe un usuario aparte del que ya tiene asignado el trabajo, se lo damos a ese.
    if len(empAEvaluar) == 1:
        print("Unicamente existe un user aparte del que ya está asignado")
        nuevoUserAsig = Usuarios.objects.get(pk=empAEvaluar[0]['usuarioAsignado'])
        segTrabajo.ultUserAsig = nuevoUserAsig
        segTrabajo.save()
        trabajo.usuarioAsignado = Usuarios.objects.get(pk=nuevoUserAsig.id)
        trabajo.save()

    # Si no hay emps ademas del que ya está encargado, reportamos
    elif len(empAEvaluar) == 0:
        print("no hay emps para asignar")
        titulo = "Trabajo atrasado sin usuario al cual asignar."
        descripcion = "El trabajo Nro° " + str(trabajo.id) + " se encuentra atrasado" \
                      "según su prioridad y no hay usuario a quien re-asignarselo."
        notificarSistema(titulo, descripcion)

    # Si hay candidatos, evaluamos
    elif len(empAEvaluar) > 1:                                          # Primer criterio
        print("primer criterio")
        empSeleccionados = []
        auxEmp = empAEvaluar[0]
        for emp in empAEvaluar:
            if emp['count'] < auxEmp['count']:
                auxEmp = emp
        for emp in empAEvaluar:
            if emp['count'] == auxEmp['count']:
                empSeleccionados.append(emp)
        print("Empleados seleccionados: " + str(empSeleccionados))
        if not eleccionUnitaria(empSeleccionados, segTrabajo):          # Segundo criterio
            print("segundo criterio")
            listadoAvances = []
            for emp in empSeleccionados:
                avanceXEmp = avanceTotalizado(emp)
                auxAvances = {
                    'usuarioAsignado': emp['usuarioAsignado'],
                    'avance': avanceXEmp,
                }
                listadoAvances.append(auxAvances)
            print(listadoAvances)
            empSeleccionados = []
            mayorAvance = listadoAvances[0]
            for emp in listadoAvances:
                if emp['avance'] > mayorAvance['avance']:
                    mayorAvance = emp
            for emp in listadoAvances:
                if emp['avance'] == mayorAvance['avance']:
                    empSeleccionados.append(emp)
            print("Empleados seleccionados: " + str(empSeleccionados))
            if not eleccionUnitaria(empSeleccionados, segTrabajo):      # Tercer criterio
                print("tercer criterio")
                listEmpSel = []
                empSeleccionado = random.choice(empSeleccionados)
                listEmpSel.append(empSeleccionado)
                eleccionUnitaria(listEmpSel, segTrabajo)



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
    print(len(empSeleccionados))
    print(empSeleccionados)
    if len(empSeleccionados) == 1:
        nuevoUserAsig = Usuarios.objects.get(pk=empSeleccionados[0]['usuarioAsignado'])
        print("Nuevo user asignado para trabajo " + str(segTrabajo.trabajo.id) + " es " + str(nuevoUserAsig))
        segTrabajo.ultUserAsig = nuevoUserAsig
        segTrabajo.save()
        print("Trabajo " + str(segTrabajo.trabajo.id) + "re-asignado desde user " + str(segTrabajo.inicialUserAsig) + " a user " + str(segTrabajo.ultUserAsig))
        trab = Trabajos.objects.get(pk=segTrabajo.trabajo.id)
        trab.usuarioAsignado = Usuarios.objects.get(pk=nuevoUserAsig.id)
        trab.save()
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


# Obtiene todos los usuarios que pueden realizar trabajos y luego vé cuantos trabajos tiene asignad ocada uno
def eleccionUsuarios(userTrabajo):
    empsAEvaluar = []
    tiposUser = TiposUsuarios.objects.filter(realizaTrabajos=True)
    users = Usuarios.objects.filter(tipoUsuario__in=tiposUser).exclude(pk=userTrabajo.id)
    estados = EstadoParametros.objects.last()
    estados_filter = [estados.estadoEspecial.id, estados.estadoInicial.id, estados.estadoPlanificado.id]
    for u in users:
        t_asig = Trabajos.objects.filter(usuarioAsignado=u, estadoTrabajo__in=estados_filter)
        dict_users = {'usuarioAsignado': str(u.id), 'count': len(t_asig), }
        empsAEvaluar.append(dict_users)
    print(empsAEvaluar)
    return empsAEvaluar


