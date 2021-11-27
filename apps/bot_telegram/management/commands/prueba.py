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


# Obtención de todos los usuarios que pueden realizar trabajos y cuantos trabajos tiene cada uno.
from .logica_pedidos_auto import *


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
##                                          ______LIMPIEZA DE DATOS________
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
                    # Nos interesa si hay repetidos o no (está bien que haya)
                    prodInicial = grupo[0]
                    minimo = prodInicial.costo
                    for g in grupo:
                        if g.costo <= minimo:
                            minimo = g.costo
                    for g in grupo:
                        if g.costo == minimo:
                            productos_def.append(g)

##                                          ______REAGRUPAMIENTO DE DATOS________
            # Identificamos cuantos proveedores quedaron luego de la etapa de selección
            proveedores = []
            produc_only = []
            for p in productos_def:
                if p.pedidoSolicitudProveedor.proveedor not in proveedores:
                    proveedores.append(p.pedidoSolicitudProveedor.proveedor)
                produc_only.append(p.producto)

            # Identificamos los productos que se repiten en el listado depurado (los que tienen igual precio)
            prod_dup = []
            for key in Counter(produc_only).keys():
                if Counter(produc_only)[key] > 1:
                    prod_dup.append(key)

            # Sumarizamos datos en dos listas de diccionarios
            prov_det = []
            prod_det_original = []
            for p in proveedores:
                cant_prod = 0
                productos = []
                for prod in productos_def:
                    if p == prod.pedidoSolicitudProveedor.proveedor:
                        cant_prod += 1
                        productos.append(prod.producto)
                prov_det.append({
                    'proveedor': p,
                    'cant_prod': cant_prod,
                    'productos': productos,
                })
                prod_det_original.append({
                    'proveedor': p,
                    'cant_prod': cant_prod,
                    'productos': productos,
                })

            for item_prod in prod_dup:                          # PRIMER CRITERIO
                for det in prov_det:
                    if len(det['productos']) == 1:
                        if item_prod == det['productos'][0]:
                            print("BORRAMOS")
                            det['productos'].remove(item_prod)
                            det['cant_prod'] = 0

            if len(prod_dup) >= 1:                              # Análisis del resto de criterios
                for item_prod in prod_dup:
                    prov_det = cambioProveedor(item_prod, prov_det, prod_det_original)

            #Rearmamos la lista depurado con los criterios. Nos interesa que los productos sean objetos tipo DetalleSolicitudProveedor
            for p in prov_det:
                prov_det_obj = []
                for prod_obj in p['productos']:
                    for det_obj_SoliProveedor in detalles:
                        if prod_obj == det_obj_SoliProveedor.producto and p['proveedor'] == det_obj_SoliProveedor.pedidoSolicitudProveedor.proveedor:
                            prov_det_obj.append(det_obj_SoliProveedor)
                p['productos'] = prov_det_obj

            # ________________ ANALISIS DE CANTIDADES________________
            prods_a_agregar = []
            for det in prov_det:
                for det_obj in det['productos']:
                    prods_candidatos = []
                    cant_pedido_original = DetallePedidoSolicitud.objects.get(pedido=det_obj.pedidoSolicitudProveedor.pedidoSolicitud,
                                                                              producto=det_obj.producto)
                    # Si la cantidad que nos propusieron es menor a la cant necesaria, entra
                    if det_obj.cantidad < cant_pedido_original.cantidad:
                        # Obtenemos la cantidad de prod que faltan para completar el pedido y generamos una list de prods_candidatos
                        diferencia = abs(det_obj.cantidad - cant_pedido_original.cantidad)
                        for dd in detalles:
                            if dd.pedidoSolicitudProveedor.proveedor != det_obj.pedidoSolicitudProveedor.proveedor and \
                                    dd.producto == det_obj.producto:
                                prods_candidatos.append(dd)
                        # Si existe al menos un prod_candidato, ordenamos la lista por costo y agregamos segun corresponda
                        if len(prods_candidatos) >= 1:
                            prods_candidatos.sort(key=costo)
                            cant_aux = det_obj.cantidad
                            for pc in prods_candidatos:
                                if (pc.cantidad + cant_aux) < cant_pedido_original.cantidad:
                                    cant_aux += pc.cantidad
                                    prods_a_agregar.append(pc)
                                elif (pc.cantidad + cant_aux) >= cant_pedido_original.cantidad:
                                    pc.cantidad = abs(cant_aux - cant_pedido_original.cantidad)
                                    prods_a_agregar.append(pc)
                                    break
            # Agregamos los nuevos productos que completan las cantidades
            for det in prov_det:
                for prod in prods_a_agregar:
                    if prod.pedidoSolicitudProveedor.proveedor == det['proveedor']:
                        det['productos'].append(prod)

            # Actualización de cant_prod lista
            for d in prov_det:
                d['cant_prod'] = len(d['productos'])



""" Función que realiza el análisis de productos
    en donde los proveedores respondieron con el mismo precio. """

def cambioProveedor(producto_item, prod_det, prod_det_original):
    # Obtenemos una lista de los proveedores que ofrecen dicho producto
    prov_ofrece = []
    for det in prod_det_original:
        if producto_item in det['productos']:
            prov_ofrece.append(det['proveedor'])


    # Encontramos al proveedor con el mayor plazo
    prov_plazos_iguales = []
    prov_min_plazo = prov_ofrece[0]
    for p in prov_ofrece:
        if p.plazoCtaCte >= prov_min_plazo.plazoCtaCte:
            prov_min_plazo = p

    # Comprobamos si no existe más de un proveedor con el plazo mínimo
    for p in prov_ofrece:
        if prov_min_plazo.plazoCtaCte == p.plazoCtaCte:
            prov_plazos_iguales.append(p)

    if len(prov_plazos_iguales) == 1:                           # Si existe un único proveedor con un plazo mínimo, entramos [SEGUNDO CRITERIO]
        for d in prod_det:
            if d['proveedor'] != prov_plazos_iguales[0]:
                for dp in d['productos']:
                    if dp == producto_item:
                        d['productos'].remove(dp)
    else:
        # Encontramos al proveedor que menos productos tiene
        prov_prod_iguales = []
        prov_min_prod = prod_det_original[0]
        for p in prod_det_original:
            if p['proveedor'] in prov_ofrece:
                if p['cant_prod'] < prov_min_prod['cant_prod']:
                    prov_min_prod = p

        # Comprobamos si no existe más de un proveedor con mínima cantidad de productos
        for p in prod_det_original:
            if p['cant_prod'] == prov_min_prod['cant_prod']:
                prov_prod_iguales.append(p)

        if len(prov_prod_iguales) == 1:                         # Si existe un único proveedor con cant productos mínimo, entramos [TERCER CRITERIO]
            for d in prod_det:
                if d['proveedor'] != prov_prod_iguales[0]['proveedor']:
                    for dp in d['productos']:
                        if dp == producto_item:
                            d['productos'].remove(dp)
        else:                                                    # Random. [CUARTO CRITERIO]
            prov_random = random.choice(prov_ofrece)
            for d in prod_det:
                if d['proveedor'] != prov_random:
                    for dp in d['productos']:
                        if dp == producto_item:
                            d['productos'].remove(dp)
#
    for d in prod_det:                                      # Actualización de lista
        d['cant_prod'] = len(d['productos'])
    return prod_det

# Funcion que analiza si las cantidades que respondieron los proveedores satisfacen la solucitd de pedio.
# Si no lo hacen, rearma el pedido.
def analisisCantidades(prod_det):
    return True