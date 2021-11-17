from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import hashlib
import random

# Para remover duplicados
import itertools

from apps.erp.models import PedidosSolicitud, DetallePedidoSolicitud, \
    Productos, PedidoSolicitudProveedor, DetallePedidoSolicitudProveedor, Pedidos

from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos
from django.contrib.auth.models import Group
from django.forms import model_to_dict
from django.urls import reverse


# Obtención de todos los usuarios que pueden realizar trabajos y cuantos trabajos tiene cada uno.
class Command(BaseCommand):
    def handle(self, *args, **options):

        # RECORDATORIO: Este proceso se ejecuta únicamente cuando se vence el plazo para respuestas.

        group_det_no_ordenado = []
        group_det_ordenado = []
        detalles = []


        respuestas = PedidoSolicitudProveedor.objects.filter(respuesta__isnull=False)
        # Solamente analizamos SI HAY respuetas.
        if len(respuestas) != 0:

            # Se obtienen TODOS los detalles de TODAS las solicitudes que se hayan respondido
            for r in respuestas:
                detalleRespuesta = DetallePedidoSolicitudProveedor.objects.filter(pedidoSolicitudProveedor=r)
                for d in detalleRespuesta:
                    detalles.append(d)

            # Se agrupan los detalles POR PRODUCTO (lista de listas)
            for d in detalles:
                aux_list = []
                for dd in detalles:
                    if d.producto == dd.producto:
                        aux_list.append(dd)
                group_det_no_ordenado.append(aux_list)

            # Removemos repetidos
            for elem in group_det_no_ordenado:
                if elem not in group_det_ordenado:
                    group_det_ordenado.append(elem)

            # # Análisis de cada grupo
            # for grupo in group_det_ordenado:
            #     if len(grupo) == 1: # Solamente un proveedor respondió por un producto en particular.
            #         prod = grupo[0]
            #         generarDetalle(prod.costo, prod.cantidad, prod.subtotal, prod.pedidoSolicitudProveedor)
            #     for g in grupo:

