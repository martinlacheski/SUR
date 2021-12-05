# Hash
import hashlib

#random
import random

# Django y models
import datetime

from apps.erp.models import Proveedores
from apps.pedidos.models import PedidoSolicitudProveedor, DetallePedidoSolicitudProveedor, PedidosSolicitud, DetallePedidoSolicitud
from django.core.mail import send_mail
from django.conf import settings
from apps.bot_telegram.logicaBot import notificarSistema
from django.urls import reverse
from apps.parametros.models import Empresa


"""     Función que crea, por cada proveedor, una cabecera y un detalle de
        todos los productos que se necesitan.
        también, a cada uno, envía un mail con un link para que
        éste pueda acceder y EDITAR los registros que le corresponden. """
def crearSolicitudes(pedido, dominio):

    # Obtenemos la url interna (/pedidos/solicitudes/proveedores/ en este caso)
    empresa = Empresa.objects.all().last()
    path_interno = reverse('pedidos:pedidos_solicitudes_proveedores_create', args=['a'])[:-1]

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
        SP.enviado = datetime.datetime.now()
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

        # Enviamos mail
        try:
            print("envio")
            print('Hola! Desde ' + str(empresa.razonSocial) +' hemos elaborado una lista de los productos' +
                        ' que estamos necesitando. Por favor entrá al link e indicanos qué productos tenes' +
                        ' dispononibles junto a su cotizacón de manera tal que podamos elaborar un pedido. \n\n ' +
                        'LINK: ' + link)
            print(prov.email)
            print(settings.EMAIL_HOST_USER)
            send_mail(subject='Solicitud de pedidos SUR EXPRESS',
                message=str('Hola! Desde ' + str(empresa.razonSocial) +' hemos elaborado una lista de los productos' +
                        ' que estamos necesitando. Por favor entrá al link e indicanos qué productos tenes' +
                        ' disponibles junto a su cotización de manera tal que podamos elaborar un pedido. \n\n ' +
                        'LINK: ' + link +'\n\nTe recomendamos que hagas clic en el símbolo ❓ para obtener un paso'
                        ' a paso de cómo cotizar tus productos.'),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[prov.email])
        except Exception as e:
            print(str(e))
            # Si falla, notificamos por sistema
            titulo = "No se pudo notificar al proveedor"
            desc = "Ha ocurrido un problema al enviar un mail al proveedor. Asegúrese de estar\"" \
                   "conectado a internet o comúniquese con el administrador"
            notificarSistema(titulo, desc)

            # Borramos la solicitud. Si no le avisó al proveedor no tiene sentido mantener el registro.
            detDel = DetallePedidoSolicitudProveedor.objects.filter(pedidoSolicitudProveedor=pedido.id)
            for d in detDel:
                d.delete()
            SP.delete()

def generarHash():
    code = random.randint(1, 10000000000)
    code = str(code).encode()
    hash_local = hashlib.sha256(code).hexdigest()
    return str(hash_local)







