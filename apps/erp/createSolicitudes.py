# Hash
import hashlib

#random
import random

# Django y models
from apps.erp.models import Proveedores
from apps.erp.models import PedidoSolicitudProveedor, DetallePedidoSolicitudProveedor, PedidosSolicitud, DetallePedidoSolicitud
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from apps.bot_telegram.logicaBot import notificarSistema
from django.urls import reverse


def crearSolicitudes(pedido, dominio):
    # Obtenemos la url interna (/pedidos/solicitudes/proveedores/ en este caso)
    path_interno = reverse('erp:pedidos_solicitudes_proveedores_create', args=['a'])[:-1]

    for prov in Proveedores.objects.all():
        # Generamos un hash por proveedor
        hash = generarHash()

        # Creamos la solicitud con su correspondiente detalle
        SP = PedidoSolicitudProveedor()
        SP.pedidoSolicitud = pedido
        SP.proveedor = prov
        SP.subtotal = pedido.subtotal
        SP.iva = pedido.iva
        SP.total = pedido.total
        SP.enviado = timezone.now()
        SP.hash = hash                          #importante
        SP.save()
        for p in DetallePedidoSolicitud.objects.filter(pedido=pedido.id):
            detSP = DetallePedidoSolicitudProveedor()
            detSP.pedidoSolicitudProveedor = SP
            detSP.producto = p.producto
            detSP.costo = p.costo
            detSP.subtotal = p.subtotal
            detSP.cantidad = p.cantidad
            detSP.save()

        link = dominio + path_interno + hash

        # # Enviamos mail
        # try:
        #     print("envio")
        #     send_mail(
        #         subject='Solicitud de pedidos SUR EXPRESS',
        #         message='Hemos elaborado un pedido, por favor entrá al link e indicanos qué tenes: \n\n ' + link,
        #         from_email=settings.EMAIL_HOST_USER,
        #         recipient_list=['ingraquelespindola@gmail.com'],
        #         )
        # except Exception as e:
        #     print(str(e))
        #     print("algo")
        #     # Si falla, notificamos por sistema
        #     titulo = "No se pudo notificar al proveedor"
        #     desc = "Ha ocurrido un problema al enviar un mail al proveedor. Asegúrese de estar\"" \
        #            "conectado a internet o comúniquese con el administrador"
        #     notificarSistema(titulo, desc)
        #
        #     # Borramos la solicitud. Si no le avisó al proveedor no tiene sentido mantener el registro.
        #     detDel = DetallePedidoSolicitudProveedor.objects.filter(pedidoSolicitudProveedor=pedido.id)
        #     for d in detDel:
        #         d.delete()
        #     SP.delete()

def generarHash():
    code = random.randint(1, 10000000000)
    code = str(code).encode()
    hash_local = hashlib.sha256(code).hexdigest()
    return str(hash_local)







