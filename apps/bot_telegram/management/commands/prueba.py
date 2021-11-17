from filecmp import cmp

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.utils import timezone
from apps.usuarios.models import Usuarios
from operator import itemgetter
import operator

from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos
from django.contrib.auth.models import Group
from django.forms import model_to_dict
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, DecimalField, IntegerField, Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.views.generic import TemplateView

from apps.erp.models import Ventas, DetalleProductosVenta, Productos, Servicios, DetalleServiciosVenta, Clientes
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import Modelos
from apps.trabajos.models import Trabajos

# Obtención de todos los usuarios que pueden realizar trabajos y cuantos trabajos tiene cada uno.
class Command(BaseCommand):
    def handle(self, *args, **options):
        datos = []
        totalVentas = 0
        totalTrabajos = 0
        fecha_inicio_actual = datetime.now() - relativedelta(months=12)
        for cli in Clientes.objects.all():
            trabajos_filtrados = Trabajos.objects.filter(fechaSalida__gte=fecha_inicio_actual).filter(
                cliente_id=cli.id)
            totalTrabajos = len(trabajos_filtrados)
            ventas_filtradas = Ventas.objects.filter(fecha__gte=fecha_inicio_actual).filter(
                cliente_id=cli.id)
            cantVentas = len(ventas_filtradas)
            for vent in ventas_filtradas:
                totalVentas += vent.total
            if totalVentas > 0:
                datos.append({
                    'cliente': cli.razonSocial,
                    'totales': float(totalVentas),
                    'ventas': cantVentas,
                    'trabajos': totalTrabajos
                })
            cantVentas = 0
            totalVentas = 0
            totalTrabajos = 0
        print(datos)
        print()
        print(sorted(datos, key=itemgetter('totales'), reverse=True))
        #print(sorted(datos, key=lambda k: k['totales']))




