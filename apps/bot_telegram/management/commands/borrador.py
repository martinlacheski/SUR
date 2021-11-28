from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import hashlib
import random

# Para remover duplicados
import itertools

# para hallar duplicados
from collections import Counter

from apps.erp.models import PedidosSolicitud, DetallePedidoSolicitud, \
    Productos, PedidoSolicitudProveedor, DetallePedidoSolicitudProveedor, Pedidos

from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos
from django.contrib.auth.models import Group
from django.forms import model_to_dict
from django.urls import reverse
from . import logica_pedidos_auto


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Se debe integrar al proceso final
        soli_no_analizadas = PedidosSolicitud.objects.filter(analizado__isnull=True)
        print(soli_no_analizadas)
        for soli in soli_no_analizadas:
            respuestas = PedidoSolicitudProveedor.objects.filter(respuesta__isnull=False, pedidoSolicitud=soli.id)
            print(respuestas)

