from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import hashlib
import random
from django.core.mail import EmailMultiAlternatives

# Para remover duplicados
import itertools

# para hallar duplicados
from collections import Counter

from apps.erp.models import Proveedores
from apps.parametros.models import EstadoParametros, Empresa
from apps.pedidos.models import Pedidos, DetallePedido
from apps.trabajos.models import Trabajos
from django.contrib.auth.models import Group
from django.forms import model_to_dict
from django.urls import reverse
from . import logica_pedidos_auto


class Command(BaseCommand):
    def handle(self, *args, **options):
        pedido = Pedidos.objects.get(pk=1)
        detalle = DetallePedido.objects.filter(pedido=pedido)
        empresa = Empresa.objects.all().last()
        prov = Proveedores.objects.get(pk=1)

        empresa = Empresa.objects.all().last()
        subject, from_email, to = 'Pedido de productos', settings.EMAIL_HOST_USER, 'leoquiroga221@gmail.com'
        text_content = 'This is an important message.'
        html_content = '<p>Hola, desde ' + empresa.razonSocial + ', a continuación listamos los productos que' \
                       ' necesitamos: <br><br>' +\
                       '<table style="margin: 0px auto; border: 1px solid black;">' \
                       ' <tr align=Center style="border: 1px solid black;"> <th>Producto</th> <th>Marca Ofertada</th> <th>Cantidad</th></tr>'

        for d in detalle:
            marca_ofertada = d.marcaOfertada
            if not marca_ofertada:
                marca_ofertada = ''
            html_content += '<tr align=Center style="border: 1px solid black;"> ' \
                                '<td style="border: 1px solid black;">' + str(d.producto.descripcion) + '</td>' + '<td style="border: 1px solid black;">' + marca_ofertada + '</td>' + '<td style="border: 1px solid black;">'+ str(d.cantidad) +'</td>' +\
                            '</tr>'
        html_content += '</table>'

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

