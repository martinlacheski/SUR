from django.db import models
from django.forms import model_to_dict

from apps.geografico.models import Localidades
from apps.parametros.models import TiposIVA, CondicionesIVA
from config.settings import MEDIA_URL, STATIC_URL


class Categorias(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    abreviatura = models.CharField(max_length=25, verbose_name='Abreviatura')

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
    abreviatura = models.CharField(max_length=25, null=True, blank=True, verbose_name='Abreviatura')
    codigo = models.CharField(max_length=20, null=True, blank=True, verbose_name='Codigo')
    codigoProveedor = models.CharField(max_length=20, null=True, blank=True, verbose_name='Codigo de Proveedor')
    codigoBarras1 = models.CharField(max_length=20, null=True, blank=True, verbose_name='Codigo de Barras 1')
    codigoBarras2 = models.CharField(max_length=20, null=True, blank=True, verbose_name='Codigo de Barras 2')
    stockReal = models.IntegerField(default=0, verbose_name='Stock Real')
    stockMinimo = models.PositiveIntegerField(default=0, verbose_name='Stock Mínimo')
    reposicion = models.PositiveIntegerField(default=0, verbose_name='Pedido Reposición')
    costo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de Costo')
    utilidad = models.DecimalField(default=30, max_digits=9, decimal_places=2, verbose_name='Margen de Utilidad')
    iva = models.ForeignKey(TiposIVA, models.DO_NOTHING, verbose_name='Tipo de IVA')
    precioVenta = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de Venta')
    imagen = models.ImageField(upload_to='productos/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    ubicacion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Ubicacion Física')
    observaciones = models.CharField(max_length=100, null=True, blank=True, verbose_name='Observaciones')
    esInsumo = models.BooleanField(default=False, verbose_name='¿Es Insumo?')

    # proveedorPrincipal = models.ForeignKey(Proveedores, models.DO_NOTHING, verbose_name='Proveedor Principal', null=True, blank=True)
    # proveedorSecundario = models.ForeignKey(Proveedores, models.DO_NOTHING, verbose_name='Proveedor Secundario', null=True, blank=True)

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
        unique_together = [['subcategoria', 'descripcion']]
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
            self.codigoBarras2 = self.codigoBarras2.upper()
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
    codigo = models.CharField(max_length=20, verbose_name='Codigo', unique=True)
    costo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de Costo')
    iva = models.ForeignKey(TiposIVA, models.DO_NOTHING, verbose_name='Tipo de IVA')
    precioVenta = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de Venta')
    imagen = models.ImageField(upload_to='servicios/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')

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


#   Clase Clientes
class Clientes(models.Model):
    razonSocial = models.CharField(max_length=100, verbose_name='Razón Social')
    condicionIVA = models.ForeignKey(CondicionesIVA, models.DO_NOTHING, verbose_name='Condición frente al IVA')
    cuil = models.CharField(max_length=11, verbose_name='Cuil')
    localidad = models.ForeignKey(Localidades, models.DO_NOTHING, verbose_name='Localidad')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    telefono = models.CharField(max_length=100, verbose_name='Teléfono')
    email = models.EmailField(max_length=254, verbose_name='Dirección de correo electrónico')
    ctaCte = models.BooleanField(default=False, verbose_name='¿Permitir Cuenta Corriente?')
    limiteCtaCte = models.DecimalField(default=0.00, max_digits=9, decimal_places=2,  null=True, blank=True, verbose_name='Límite de Cuenta Corriente')
    plazoCtaCte = models.TimeField(verbose_name='Plazo de Vencimiento Cuenta Corriente', null=True, blank=True)

    def toJSON(self):
        item = model_to_dict(self)
        item['condicionIVA'] = self.condicionIVA.toJSON()
        item['localidad'] = self.localidad.toJSON()
        item['limiteCtaCte'] = format(self.limiteCtaCte, '.2f')
        # item['plazoCtaCte'] = self.plazoCtaCte.strftime('%dd/%MM/%yyyy')
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
        super(Clientes, self).save(force_insert, force_update)