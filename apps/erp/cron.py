from apps.erp.models import Productos
from apps.erp.models import PedidosSolicitud, DetallePedidoSolicitud
from apps.erp.models import PedidoSolicitudProveedor, DetallePedidoSolicitudProveedor
from apps.erp.models import PedidosSolicitud, DetallePedidoSolicitud
from django.utils import timezone

def generarSolicitudPedido():
    sub_total = 0
    productos_stock_min = []
    pedido = PedidosSolicitud()

    for producto in Productos.objects.all():
        if producto.stockReal < producto.stockMinimo and producto.reposicion > 0:
            sub_total += producto.costo * producto.reposicion
            productos_stock_min.append(producto)

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

def generarPedido():
    respuestas = PedidoSolicitudProveedor.objects.filter(respuesta__isnull=False)




