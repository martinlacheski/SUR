from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import hashlib
import random

from apps.erp.models import PedidosSolicitud, DetallePedidoSolicitud, Productos

from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos
from django.contrib.auth.models import Group
from django.forms import model_to_dict
from django.urls import reverse


# Obtención de todos los usuarios que pueden realizar trabajos y cuantos trabajos tiene cada uno.
class Command(BaseCommand):
    def handle(self, *args, **options):
        print(reverse('erp:pedidos_solicitudes_proveedores_create', args=['a'])[:-1])



