from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models
from django.forms import model_to_dict
from simple_history.models import HistoricalRecords

from apps.geografico.models import Localidades
from apps.parametros.models import TiposIVA, CondicionesIVA, CondicionesPago, TiposComprobantes, TiposPercepciones, \
    MediosPago
from apps.usuarios.models import Usuarios
from config.settings import MEDIA_URL, STATIC_URL


#   Clase Clientes
class Clientes(models.Model):
    razonSocial = models.CharField(max_length=100, verbose_name='Razón Social')
    condicionIVA = models.ForeignKey(CondicionesIVA, models.DO_NOTHING, verbose_name='Condición frente al IVA')
    cuil = models.CharField(max_length=11, verbose_name='Cuil', unique=True)
    localidad = models.ForeignKey(Localidades, models.DO_NOTHING, verbose_name='Localidad')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    telefono = models.CharField(max_length=100, verbose_name='Teléfono')
    email = models.EmailField(max_length=254, verbose_name='Dirección de correo electrónico', null=True, blank=True)
    cbu = models.CharField(max_length=22, verbose_name='Clave CBU/CVU', null=True, blank=True)
    alias = models.CharField(max_length=100, verbose_name='Alias', null=True, blank=True)
    tipoPercepcion = models.ForeignKey(TiposPercepciones, models.DO_NOTHING, verbose_name='Tipo de Percepción')
    condicionPago = models.ForeignKey(CondicionesPago, models.DO_NOTHING, verbose_name='Condición de Pago')
    limiteCtaCte = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True, blank=True,
                                       verbose_name='Límite de Cuenta Corriente')
    plazoCtaCte = models.PositiveIntegerField(default=0, verbose_name='Plazo de Vencimiento', null=True, blank=True)
    chatIdCliente = models.IntegerField(null=True, blank=True, default=None)
    estado = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.razonSocial

    def toJSON(self):
        item = model_to_dict(self)
        item['condicionIVA'] = self.condicionIVA.toJSON()
        item['localidad'] = self.localidad.toJSON()
        try:
            item['tipoPercepcion'] = self.tipoPercepcion.toJSON()
        except:
            pass
        item['condicionPago'] = self.condicionPago.toJSON()
        item['limiteCtaCte'] = format(self.limiteCtaCte, '.2f')
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'erp_clientes'
        ordering = ['razonSocial']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.razonSocial = self.razonSocial.upper()
        self.direccion = self.direccion.upper()
        try:
            self.alias = self.alias.upper()
        except:
            pass
        super(Clientes, self).save(force_insert, force_update)


#   Clase Proveedores
class Proveedores(models.Model):
    razonSocial = models.CharField(max_length=100, verbose_name='Razón Social')
    condicionIVA = models.ForeignKey(CondicionesIVA, models.DO_NOTHING, verbose_name='Condición frente al IVA')
    cuit = models.CharField(max_length=11, verbose_name='Cuit', unique=True)
    localidad = models.ForeignKey(Localidades, models.DO_NOTHING, verbose_name='Localidad')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    telefono = models.CharField(max_length=100, verbose_name='Teléfono')
    email = models.EmailField(max_length=254, verbose_name='Dirección de correo electrónico')
    cbu = models.CharField(max_length=22, verbose_name='Clave CBU/CVU', null=True, blank=True)
    alias = models.CharField(max_length=100, verbose_name='Alias', null=True, blank=True)
    tipoPercepcion = models.ForeignKey(TiposPercepciones, models.DO_NOTHING, verbose_name='Tipo de Percepción')
    condicionPago = models.ForeignKey(CondicionesPago, models.DO_NOTHING, verbose_name='Condición de Pago')
    plazoCtaCte = models.PositiveIntegerField(default=0, verbose_name='Plazo de Vencimiento', null=True, blank=True)
    estado = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.razonSocial

    def toJSON(self):
        item = model_to_dict(self)
        item['condicionIVA'] = self.condicionIVA.toJSON()
        item['localidad'] = self.localidad.toJSON()
        try:
            item['tipoPercepcion'] = self.tipoPercepcion.toJSON()
        except:
            pass
        try:
            item['condicionPago'] = self.condicionPago.toJSON()
        except:
            pass
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        db_table = 'erp_proveedores'
        ordering = ['razonSocial']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.razonSocial = self.razonSocial.upper()
        self.direccion = self.direccion.upper()
        try:
            self.alias = self.alias.upper()
        except:
            pass
        super(Proveedores, self).save(force_insert, force_update)


class Categorias(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    abreviatura = models.CharField(max_length=25, verbose_name='Abreviatura')
    history = HistoricalRecords()

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        db_table = 'erp_categorias'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        self.abreviatura = self.abreviatura.upper()
        super(Categorias, self).save(force_insert, force_update)


class Subcategorias(models.Model):
    categoria = models.ForeignKey(Categorias, models.DO_NOTHING, verbose_name='Categoría')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    abreviatura = models.CharField(max_length=25, verbose_name='Abreviatura')
    history = HistoricalRecords()

    def __str__(self):
        return self.nombre
        # return self.get_full_name()

    def get_full_name(self):
        return '{} - {}'.format(self.categoria.nombre, self.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        return item

    class Meta:
        unique_together = [['categoria', 'nombre']]
        verbose_name = 'Subcategoría'
        verbose_name_plural = 'Subcategorías'
        db_table = 'erp_subcategorias'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        self.abreviatura = self.abreviatura.upper()
        super(Subcategorias, self).save(force_insert, force_update)


class Productos(models.Model):
    subcategoria = models.ForeignKey(Subcategorias, models.DO_NOTHING, verbose_name='Subcategoría')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción')
    abreviatura = models.CharField(max_length=30, verbose_name='Abreviatura')
    codigo = models.CharField(max_length=20, null=True, blank=True, verbose_name='Codigo', unique=True)
    codigoProveedor = models.CharField(max_length=20, null=True, blank=True, verbose_name='Codigo de Proveedor',
                                       unique=True)
    codigoBarras1 = models.CharField(max_length=20, null=True, blank=True, verbose_name='Codigo de Barras 1',
                                     unique=True)
    stockReal = models.IntegerField(default=0, verbose_name='Stock Real')
    stockMinimo = models.PositiveIntegerField(default=0, verbose_name='Stock Mínimo')
    reposicion = models.PositiveIntegerField(default=0, verbose_name='Pedido Reposición')
    costo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de Costo')
    utilidad = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Margen de Utilidad')
    iva = models.ForeignKey(TiposIVA, models.DO_NOTHING, verbose_name='Tipo de IVA')
    precioVenta = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de Venta')
    imagen = models.ImageField(upload_to='productos/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    ubicacion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Ubicacion Física')
    observaciones = models.CharField(max_length=100, null=True, blank=True, verbose_name='Observaciones')
    esInsumo = models.BooleanField(default=False, verbose_name='¿Es Insumo?')
    descuentaStock = models.BooleanField(default=True, verbose_name='¿Descuenta Stock?')
    history = HistoricalRecords()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} - {}'.format(self.subcategoria.nombre, self.descripcion)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = '{}/{}'.format(self.subcategoria.nombre, self.descripcion)
        item['subcategoria'] = self.subcategoria.toJSON()
        item['iva'] = self.iva.toJSON()
        item['imagen'] = self.get_image()
        item['costo'] = format(self.costo, '.2f')
        item['utilidad'] = format(self.utilidad, '.2f')
        item['precioVenta'] = format(self.precioVenta, '.2f')
        return item

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        unique_together = ['subcategoria', 'descripcion']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'erp_productos'
        ordering = ['subcategoria', 'descripcion']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        try:
            self.codigo = self.codigo.upper()
        except:
            pass
        try:
            self.codigoBarras1 = self.codigoBarras1.upper()
        except:
            pass
        try:
            self.codigoProveedor = self.codigoProveedor.upper()
        except:
            pass
        try:
            self.abreviatura = self.abreviatura.upper()
        except:
            pass
        try:
            self.ubicacion = self.ubicacion.upper()
        except:
            pass
        try:
            self.observaciones = self.observaciones.upper()
        except:
            pass
        super(Productos, self).save(force_insert, force_update)


class Servicios(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', unique=True)
    codigo = models.CharField(max_length=30, verbose_name='Codigo', unique=True)
    costo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de Costo')
    iva = models.ForeignKey(TiposIVA, models.DO_NOTHING, verbose_name='Tipo de IVA')
    precioVenta = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de Venta')
    esfuerzo = models.PositiveIntegerField(default=20, verbose_name='Esfuerzo')
    imagen = models.ImageField(upload_to='servicios/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    history = HistoricalRecords()

    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        item['iva'] = self.iva.toJSON()
        item['imagen'] = self.get_image()
        item['costo'] = format(self.costo, '.2f')
        item['precioVenta'] = format(self.precioVenta, '.2f')
        return item

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        db_table = 'erp_servicios'
        ordering = ['descripcion']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        self.codigo = self.codigo.upper()
        super(Servicios, self).save(force_insert, force_update)


#   Clase Ventas
class Ventas(models.Model):
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario')
    fecha = models.DateField(verbose_name='Fecha')
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING, verbose_name='Cliente')
    condicionVenta = models.ForeignKey(CondicionesPago, models.DO_NOTHING, verbose_name='Condición de pago')
    medioPago = models.ForeignKey(MediosPago, models.DO_NOTHING, verbose_name='Medio de pago')
    trabajo = models.CharField(default="", max_length=20, verbose_name='ID Trabajo Asociado', null=True, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    percepcion = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estadoVenta = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        # return self.cliente.razonSocial
        return self.get_full_sale()

    def get_full_sale(self):
        return '{} - {}'.format(self.fecha, self.cliente.razonSocial)

    def toJSON(self):
        item = model_to_dict(self)
        item['usuario'] = self.usuario.toJSON()
        item['cliente'] = self.cliente.toJSON()
        item['medioPago'] = self.medioPago.toJSON()
        item['condicionVenta'] = self.condicionVenta.toJSON()
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        db_table = 'erp_ventas'
        ordering = ['fecha', 'id']


# Detalle de Productos de la venta
class DetalleProductosVenta(models.Model):
    venta = models.ForeignKey(Ventas, models.DO_NOTHING)
    producto = models.ForeignKey(Productos, models.DO_NOTHING)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    history = HistoricalRecords()

    def __str__(self):
        return self.producto.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['venta'])
        item['producto'] = self.producto.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta - Productos'
        verbose_name_plural = 'Detalle de Ventas - Productos'
        db_table = 'erp_ventas_detalle_productos'
        ordering = ['id']


# Detalle de Servicios de la venta
class DetalleServiciosVenta(models.Model):
    venta = models.ForeignKey(Ventas, models.DO_NOTHING)
    servicio = models.ForeignKey(Servicios, models.DO_NOTHING)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    history = HistoricalRecords()

    def __str__(self):
        return self.servicio.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['venta'])
        item['servicio'] = self.servicio.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta - Servicios'
        verbose_name_plural = 'Detalle de Ventas - Servicios'
        db_table = 'erp_ventas_detalle_servicios'
        ordering = ['id']


#   Clase Compras
class Compras(models.Model):
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario')
    fecha = models.DateField(verbose_name='Fecha')
    proveedor = models.ForeignKey(Proveedores, models.DO_NOTHING, verbose_name='Proveedor')
    condicionPagoCompra = models.ForeignKey(CondicionesPago, models.DO_NOTHING, verbose_name='Condición de pago')
    tipoComprobante = models.ForeignKey(TiposComprobantes, models.DO_NOTHING, verbose_name='Tipo de Comprobante')
    nroComprobante = models.CharField(max_length=100, verbose_name='Número de Comprobante')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    percepcion = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estadoCompra = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.get_full_sale()

    def get_full_sale(self):
        return '{} - {}'.format(self.fecha, self.proveedor.razonSocial)

    def toJSON(self):
        item = model_to_dict(self)
        item['usuario'] = self.usuario.toJSON()
        item['proveedor'] = self.proveedor.toJSON()
        item['condicionPagoCompra'] = self.condicionPagoCompra.toJSON()
        item['tipoComprobante'] = self.tipoComprobante.toJSON()
        return item

    class Meta:
        unique_together = ['proveedor', 'tipoComprobante', 'nroComprobante']
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        db_table = 'erp_compras'
        ordering = ['fecha', 'id']


class DetalleProductosCompra(models.Model):
    compra = models.ForeignKey(Compras, models.DO_NOTHING)
    producto = models.ForeignKey(Productos, models.DO_NOTHING)
    costo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    history = HistoricalRecords()

    def __str__(self):
        return self.producto.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['compra'])
        item['producto'] = self.producto.toJSON()
        item['costo'] = format(self.costo, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'
        db_table = 'erp_compras_detalle'
        ordering = ['id']
