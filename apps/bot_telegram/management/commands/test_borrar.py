import datetime
import random

import time
import telegram
from apscheduler.schedulers.background import BlockingScheduler
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from apps.bot_telegram.logicaBot import porcentajeTrabajo
from apps.bot_telegram.models import seguimientoTrabajos
from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos, DetalleServiciosTrabajo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.db.models import Count
from apps.usuarios.models import Usuarios
from apps.bot_telegram.logicaBot import porcentajeTrabajo


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
    print("Epleados iniciales a evaluar:\n " + str(empAEvaluar))
    #time.sleep(2.4)
    # Si unicamente existe un usuario aparte del que ya tiene asignado el trabajo, se lo damos a ese.
    if len(empAEvaluar) == 1:
        nuevoUserAsig = Usuarios.objects.get(pk=empAEvaluar[0]['usuarioAsignado'])
        segTrabajo.ultUserAsig = nuevoUserAsig
        #segTrabajo.save()

    # Si no hay emps ademas del que ya está encargado, reportamos
    elif len(empAEvaluar) == 0:
        print("Notificar a administración que el trabajo está retardado y no hay usuario a quien asignar")

    # Si hay candidatos, evaluamos
    elif len(empAEvaluar) > 1:
        empSeleccionados = []
        #       PRIMER CRITERIO
        #       (Trabajador con menos trabajos asignados)
        auxEmp = empAEvaluar[0]
        print("\n\nPRIMER CRITERIO (Trabajador con menos trabajos asignados)")
        #time.sleep(2.4)
        for emp in empAEvaluar:
            if emp['count'] < auxEmp['count']:
                auxEmp = emp
        print("La menor cantidad de trabajos en un empleado es: " + str(auxEmp['count']))
        #time.sleep(2.4)
        for emp in empAEvaluar:
            if emp['count'] == auxEmp['count']:
                empSeleccionados.append(emp)
        print("Empleados seleccionados: " + str(empSeleccionados))
        #time.sleep(2.4)
        if not eleccionUnitaria(empSeleccionados, segTrabajo):
            print("\n\nSEGUNDO CRITERIO (Trabajador con mayor avance en totalidad de trabajos)")
            #time.sleep(2.4)
            #       SEGUNDO CRITERIO
            #       (   Trabajador con mayor avance en totalidad de trabajos.
            #           Se asume que todos tienen la misma cantidad de trabajos
            #           debido al primer criterio.
            #        )
            listadoAvances = []
            for emp in empSeleccionados:
                avanceXEmp = avanceTotalizado(emp)
                print("Evaluando empleado " + str(emp['usuarioAsignado']) + " tiene cantAvanceTotal " + str(avanceXEmp))
                #time.sleep(2.4)
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
            print("Este es el mayor avance entre los postulantes: ", str(mayorAvance['avance']))
            #time.sleep(2.4)
            for emp in listadoAvances:
                if emp['avance'] == mayorAvance['avance']:
                    empSeleccionados.append(emp)
            print("Estos son los empleados seleccionados del segundo criterio: " + str(empSeleccionados))
            #time.sleep(2.4)
            if not eleccionUnitaria(empSeleccionados, segTrabajo):
                #   TERCER CRITERIO
                #   (Random. Elegimos cualquiera de los postulantes)
                print("\n\nTERCER CRITERIO")
                empRandom = random.choice(empSeleccionados)
                if not empRandom['usuarioAsignado']:
                    print("No se puede elegir a un usuario NONE. SE EMPIEZA OTRA VEZ. \n\n\n")
                    reasignacionTrabajo(trabajo)
                else:
                    print("El empleado elegido es: " + str(empRandom))

def avanceTotalizado(empleado):
    estados = EstadoParametros.objects.last()
    estados_filter = [estados.estadoEspecial.id, estados.estadoInicial.id, estados.estadoPlanificado.id]
    trabajosEmp = Trabajos.objects.filter(usuarioAsignado=empleado['usuarioAsignado'], estadoTrabajo__in=estados_filter)
    avance = 0
    for t in trabajosEmp:
        avance += float(porcentajeTrabajo(t))
    return avance

def eleccionUnitaria(empSeleccionados, segTrabajo):
    if len(empSeleccionados) == 1:
        if not (empSeleccionados[0]['usuarioAsignado']):
            print("usuario NONE")
        else:
            print("Le asignamos al usuario " + str(empSeleccionados[0]) + " el trabajo " + str(segTrabajo.trabajo.id))
            #time.sleep(2.4)
            nuevoUserAsig = Usuarios.objects.get(pk=empSeleccionados[0]['usuarioAsignado'])
            segTrabajo.ultUserAsig = nuevoUserAsig
            #segTrabajo.save()
            return True
    else:
        print("No se cumplió el criterio. Se pasa al siguiente")
        #time.sleep(2.4)
        return False

trab = Trabajos.objects.get(pk=62)
reasignacionTrabajo(trab)