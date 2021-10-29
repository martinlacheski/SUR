import datetime

from django_cron import CronJobBase, Schedule
from apps.trabajos.models import Trabajos
from apps.bot_telegram.models import seguimientoTrabajos
from apps.parametros.models import EstadoParametros


class rastreoTrabajos(CronJobBase):
	RUN_EVERY_MINS = 1440

	estados = EstadoParametros.objects.get().last()
	estados_excluidos = [estados.estadoFinalizado.id,
	                     estados.estadoEntregado.id,
	                     estados.estadoCancelado.id]
	trabajos = Trabajos.objects.exclude(estadoTrabajo__in=estados_excluidos)

	for t in trabajos:
		cant_dias_en_proceso = datetime.date.today() - t.fechaEntrada
		if cant_dias_en_proceso > t.prioridad.plazoPrioridad:
			print("Enviar msj")
			print("Programar job a la espera de en 1h").
