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
from .logica_pedidos_auto import ver_detalle


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
                    # Nos interesa si hay repetidos o no.
                    prodInicial = grupo[0]
                    minimo = 0
                    for g in grupo:
                        if g.costo <= prodInicial.costo:
                            minimo = g.costo
                    for g in grupo:
                        if g.costo == minimo:
                            productos_def.append(g)


            for x in productos_def:
                print(str(x.producto.id) + " - " +
                      str(x.producto.abreviatura) + " - " +
                      str(x.costo) + " - " +
                      str(x.pedidoSolicitudProveedor.proveedor))

            print()
            print()

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

            # Sumarizamos datos en un diccionario
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
                prod_det_original.append(
                    {'proveedor': p,
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

            vuelta = 0
            if len(prod_dup) >= 1:                              # Análisis del resto de criterios
                for item_prod in prod_dup:
                    ver_detalle(prov_det)
                    print()
                    print()
                    print()
                    print("____________________________________________VUELTA: " + str(vuelta))
                    print("PRODUCTO A ANALIZAR: " + str(item_prod.abreviatura))

                    cambioProveedor(item_prod, prov_det, prod_det_original)
                    vuelta += 1


def cambioProveedor(producto_item, prod_det, prod_det_original):

    print("\nCOMO EMPIEZA: ")
    ver_detalle(prod_det)

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
        print("[SEGUNDO CRITERIO]")
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

        print("PROVEEDORES MISMA CANT PROD: " + str(prov_prod_iguales))
        if len(prov_prod_iguales) == 1:                         # Si existe un único proveedor con cant productos mínimo, entramos [TERCER CRITERIO]
            print("[TERCER CRITERIO]")
            for d in prod_det:
                if d['proveedor'] != prov_prod_iguales[0]['proveedor']:
                    for dp in d['productos']:
                        if dp == producto_item:
                            d['productos'].remove(dp)
                                                               # Random. [CUARTO CRITERIO]
        else:
            print("[CUARTO CRITERIO]")
            prov_random = random.choice(prov_ofrece)
            for d in prod_det:
                if d['proveedor'] != prov_random:
                    for dp in d['productos']:
                        if dp == producto_item:
                            d['productos'].remove(dp)


    print("\nCOMO TERMINA:")
    for d in prod_det:                                      # Actualización de lista
        d['cant_prod'] = len(d['productos'])
    #
    ver_detalle(prod_det)

    # prov_inicial = pd['proveedor']  # El proveedor del producto que estamos analizando
    # print("proveedor inicial:" + str(prov_inicial))
    #

    #

    #
    # print("proveedor electo:" + str(prov_selecto))
    # print(len(prov_plazos_iguales))
    #

    #

    #
    # else:
    #     print("tercer criterio (help)")
    #     # Tercer criterio (buscamos, de los prov que ofrecen dicho producto, quien es el que menos prod tiene. Si tienen igual, random)
    #     # prov_aux = prod_det[0]
    #     # for p in prod_det:
    #     #     if p['proveedor'] in prov_ofrece:
    #     #         if p['cant_prod'] < prov_aux['cant_prod']:
    #     #             prov_aux = p
    #
    #



