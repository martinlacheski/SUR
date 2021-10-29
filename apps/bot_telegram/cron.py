from django_cron import CronJobBase, Schedule
from apps.trabajos.models import Trabajos
from apps.bot_telegram.models import seguimientoTrabajos
from apps.parametros.models import EstadoParametros


class rastreoTrabajos(CronJobBase):
	RUN_EVERY_MINS = 1440

	estados = EstadoParametros.objects.get().last()
	print(estados.estadoFinalizado)
	trabajos = Trabajos.objects.exclude(estadoTrabajo=[estados.estadoFinalizado,
	                                                   estados.estadoEntregado,
	                                                   estados.estadoCancelado])
