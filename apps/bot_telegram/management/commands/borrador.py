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

        sub_total = 0
        productos_stock_min = []
        pedido = PedidosSolicitud()

        for producto in Productos.objects.all():
            if producto.stockReal < producto.stockMinimo and producto.reposicion > 0:
                sub_total += producto.costo * producto.reposicion
                productos_stock_min.append(producto)

        pedido.fecha = timezone.now().date()
        # pedido.fechaLimite = formPedidoRequest['fechaLimite'] No va a tener fecha límite si se crea mediante un cron.
        #pedido.iva = float(sub_total) * 0.21


        pedido.total = sub_total
        pedido.save()

        pedido.iva = 0
        for p in productos_stock_min:
            pedido.iva += p.costo * (p.iva.iva / 100)
            det = DetallePedidoSolicitud()
            det.pedido_id = pedido.id
            det.producto_id = p.id
            det.costo = p.costo
            det.cantidad = p.reposicion
            det.subtotal = p.costo * p.reposicion
            det.save()
        pedido.subtotal = float(sub_total) - float(pedido.iva)
        pedido.save()

        # # Se debe integrar al proceso final
        # soli_no_analizadas = PedidosSolicitud.objects.filter(analizado__isnull=True)
        # print(soli_no_analizadas)
        # for soli in soli_no_analizadas:
        #     respuestas = PedidoSolicitudProveedor.objects.filter(respuesta__isnull=False, pedidoSolicitud=soli.id)
        #     print(respuestas)

