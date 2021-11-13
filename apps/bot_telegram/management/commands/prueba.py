from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.utils import timezone

from apps.erp.models import PedidosSolicitud, DetallePedidoSolicitud, Productos

from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos
from django.contrib.auth.models import Group
from django.forms import model_to_dict

# Obtención de todos los usuarios que pueden realizar trabajos y cuantos trabajos tiene cada uno.
class Command(BaseCommand):
    def handle(self, *args, **options):
        sub_total = 0
        productos_stock_min = []
        pedido = PedidosSolicitud()

        for producto in Productos.objects.all():
            if producto.stockReal < producto.stockMinimo and producto.reposicion > 0:
                sub_total += producto.costo * producto.reposicion
                productos_stock_min.append(producto)

        print("productos: " + str(productos_stock_min))

        pedido.fecha = timezone.now().date()
        # pedido.fechaLimite = formPedidoRequest['fechaLimite'] No va a tener fecha límite si se crea mediante un cron.
        pedido.iva = float(sub_total) * 0.21
        pedido.subtotal = float(sub_total) - pedido.iva
        pedido.total = sub_total
        pedido.save()

        for p in productos_stock_min:
            det = DetallePedidoSolicitud()
            det.pedido_id = pedido.id
            det.producto_id = p.id
            det.costo = p.costo
            det.cantidad = p.reposicion
            det.subtotal = p.costo * p.reposicion
            det.save()






