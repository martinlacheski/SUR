from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.utils import timezone

from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos


class Command(BaseCommand):
    def handle(self, *args, **options):
        trabajo = Trabajos.objects.get()
        estados = EstadoParametros.objects.last()
        estados_filter = [estados.estadoEspecial.id,
                          estados.estadoInicial.id,
                          estados.estadoPlanificado.id]
        empAEvaluar = Trabajos.objects.exclude(usuarioAsignado=trabajo.usuarioAsignado). \
            values('usuarioAsignado').annotate(count=Count('id')). \
            order_by(). \
            filter(estadoTrabajo__in=estados_filter)