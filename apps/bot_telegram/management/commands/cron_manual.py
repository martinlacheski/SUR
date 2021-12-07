from django.core.management import BaseCommand
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

class Command(BaseCommand):
    def handle(self, *args, **options):
        estados = EstadoParametros.objects.last()
        estados_excluidos = [estados.estadoFinalizado.id, estados.estadoEntregado.id, estados.estadoCancelado.id]
        trabajos = Trabajos.objects.exclude(estadoTrabajo__in=estados_excluidos)
        trabajosASupervisar = []
        for t in trabajos:
            cant_dias_en_proceso = datetime.date.today() - t.fechaEntrada
            # Si la cantidad de días desde que el trabajo está en la empresa es mayor a su plazo aproximado, hacemos cosas
            if cant_dias_en_proceso.days > t.prioridad.plazoPrioridad:
                try:
                    # Si ya existe un seguimiento para el trabajo en cuestión, ponemos su cant notif diaria a 0
                    segTrab = seguimientoTrabajos.objects.get(trabajo=t)
                    print("tenía seguimiento")
                    segTrab.cantVecesNotif_dia = 0
                    segTrab.respuestaUser = None
                    segTrab.notif_por_sist = 0
                except ObjectDoesNotExist:
                    print("no tenía seguimiento")
                    # Si no existe, creamos un seguimiento
                    segTrab = seguimientoTrabajos()
                    segTrab.trabajo = t
                    segTrab.inicialUserAsig = t.usuarioAsignado
                    segTrab.cantVecesNotif_dia = 0
                    segTrab.notif_por_sist = 0
                segTrab.save()
                trabajosASupervisar.append(t)
        # Si hay trabajos para supervisar, creamos un job.
        #if trabajosASupervisar:
            #CommandCron.job(self, trabajosASupervisar)
