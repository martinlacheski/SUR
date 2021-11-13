from apps.erp.models import Productos, DetallePedidoSolicitud
from apps.erp.models import PedidosSolicitud
from django.utils import timezone

def generarSolicitudPedido():
    sub_total = 0
    productos_stock_min = []
    pedido = PedidosSolicitud()


    for producto in Productos.objects.all():
        if producto.stockReal < producto.stockMinimo and producto.reposicion > 0:
            sub_total += producto.costo
            productos_stock_min.append(producto)

    print("productos: " + str(productos_stock_min))

    pedido.fecha = timezone.now().date()
    # pedido.fechaLimite = formPedidoRequest['fechaLimite'] No va a tener fecha límite si se crea mediante un cron.
    pedido.subtotal = sub_total
    pedido.iva = sub_total * 0.21
    pedido.total = sub_total + pedido.iva
    pedido.save()

    for p in productos_stock_min:
        det = DetallePedidoSolicitud()
        det.pedido_id = pedido.id
        det.producto_id = p.id
        det.costo = p.costo
        det.cantidad = p.reposicion
        det.subtotal = p.costo * p.reposicion
        det.save()

