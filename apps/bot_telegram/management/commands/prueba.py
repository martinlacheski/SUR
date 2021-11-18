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

        detalles = []                   # Contiene los datos crudos de las respuestas
        group_det_no_ordenado = []      # Auxiliar de agrupamiento
        group_det_ordenado = []         # Productos separados por grupo (lista de listas)
        productos_def = []              # Productos finales que ENTRARÍAN en el pedido. Puede contener repetidos.

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

            # Armado de lista de productos que se van a pedir
            for grupo in group_det_ordenado:
                if len(grupo) == 1:                     # si únicamente UN proveedor ofertó por el producto
                    productos_def.append(grupo[0])
                else:                                   # varios ofertaron por el producto
                    # Se halla el costo mínimo por grupo y se agregan todos los productos con ese costo.
                    # Nos interesa si hay repetidos o no.
                    prodInicial = grupo[0]
                    minimo = 0
                    for g in grupo:
                        if g.costo <= prodInicial.costo:
                            minimo = g.costo
                    for g in grupo:
                        if g.costo == minimo:
                            productos_def.append(g)


            # for x in productos_def:
            #     print(str(x.producto.id) + " - " + str(x.producto.abreviatura) + " - " + str(x.costo) + "-" + str(x.pedidoSolicitudProveedor.proveedor))

