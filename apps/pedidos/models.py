from django.db import models
from django.forms import model_to_dict
from simple_history.models import HistoricalRecords

from apps.geografico.models import Localidades
from apps.parametros.models import TiposIVA, CondicionesIVA, CondicionesPago, TiposComprobantes, TiposPercepciones, \
    MediosPago
from apps.erp.models import Productos, Proveedores
from apps.usuarios.models import Usuarios


#   Clase Pedidos de Solicitud de Productos
class PedidosSolicitud(models.Model):
    fecha = models.DateField(verbose_name='Fecha')
    fechaLimite = models.DateTimeField(verbose_name='Fecha Límite', null=True)
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario', blank=True, null=True)
    realizado = models.BooleanField(default="", blank=True, null=True)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.BooleanField(default="", blank=True, null=True)
    analizado = models.BooleanField(blank=True, null=True)
    resp_incompleta = models.BooleanField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id)

    def get_full_sale(self):
        return '{} - {}'.format(self.fecha, self.estado)

    def toJSON(self):
        item = model_to_dict(self)
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        verbose_name = 'Solicitud de Pedido'
        verbose_name_plural = 'Solicitudes de Pedidos'
        db_table = 'pedidos_solicitud'
        ordering = ['fecha', 'id']


class DetallePedidoSolicitud(models.Model):
    pedido = models.ForeignKey(PedidosSolicitud, models.DO_NOTHING)
    producto = models.ForeignKey(Productos, models.DO_NOTHING, verbose_name='Producto')
    costo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad_resp = models.IntegerField(default=0)
    history = HistoricalRecords()

    def __str__(self):
        return self.producto.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['pedido'])
        item['producto'] = self.producto.toJSON()
        item['costo'] = format(self.costo, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Solicitud de Pedido'
        verbose_name_plural = 'Detalle de Solicitudes de Pedidos'
        db_table = 'pedidos_solicitud_detalle'
        ordering = ['id']


#   Clase Solicitudo de Pedidos completado por Proveedores
class PedidoSolicitudProveedor(models.Model):
    pedidoSolicitud = models.ForeignKey(PedidosSolicitud, models.DO_NOTHING, verbose_name='Pedido de Solicitud')
    proveedor = models.ForeignKey(Proveedores, models.DO_NOTHING, verbose_name='Proveedor')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    enviado = models.DateTimeField(verbose_name='Fecha y Hora de envío correo electrónico')
    visto = models.DateTimeField(verbose_name='Fecha y Hora de visto el formulario', null=True)
    respuesta = models.DateTimeField(verbose_name='Fecha y Hora de respuesta del formulario', null=True)
    hash = models.CharField(max_length=66, verbose_name='Hash de solicitud', null=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} - {}'.format(self.pedidoSolicitud, self.proveedor)

    def toJSON(self):
        item = model_to_dict(self)
        item['pedidoSolicitud'] = self.pedidoSolicitud.toJSON()
        item['proveedor'] = self.proveedor.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        verbose_name = 'Solicitud de Pedido Proveedor'
        verbose_name_plural = 'Solicitudes de Pedidos Proveedor'
        db_table = 'pedidos_solicitud_proveedor'
        ordering = ['id']


class DetallePedidoSolicitudProveedor(models.Model):
    pedidoSolicitudProveedor = models.ForeignKey(PedidoSolicitudProveedor, models.DO_NOTHING)
    producto = models.ForeignKey(Productos, models.DO_NOTHING, verbose_name='Producto')
    marcaOfertada = models.CharField(max_length=100, verbose_name='Marca Ofertada', blank=True, null=True)
    costo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.producto.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['pedidoSolicitudProveedor'])
        item['producto'] = self.producto.toJSON()
        item['costo'] = format(self.costo, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Solicitud de Pedido'
        verbose_name_plural = 'Detalle de Solicitudes de Pedidos'
        db_table = 'pedidos_solicitud_proveedor_detalle'
        ordering = ['id']


#   Clase Pedidos
class Pedidos(models.Model):
    pedidoSolicitud = models.ForeignKey(PedidosSolicitud, models.DO_NOTHING, verbose_name='Pedido de Solicitud')
    proveedor = models.ForeignKey(Proveedores, models.DO_NOTHING, verbose_name='Proveedor')
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario', blank=True, null=True)
    fecha = models.DateField(verbose_name='Fecha')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.BooleanField(default="", blank=True, null=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} - {}'.format(self.pedidoSolicitud, self.fecha)

    def toJSON(self):
        item = model_to_dict(self)
        item['proveedor'] = self.proveedor.toJSON()
        item['pedidoSolicitud'] = self.pedidoSolicitud.toJSON()
        return item

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        db_table = 'pedidos'
        ordering = ['id']


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedidos, models.DO_NOTHING)
    producto = models.ForeignKey(Productos, models.DO_NOTHING, verbose_name='Producto')
    marcaOfertada = models.CharField(max_length=100, verbose_name='Marca Ofertada', blank=True, null=True)
    costo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.producto.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['pedido'])
        item['producto'] = self.producto.toJSON()
        item['costo'] = format(self.costo, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalle de Pedidos'
        db_table = 'pedidos_detalle'
        ordering = ['id']
