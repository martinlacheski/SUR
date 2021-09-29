from django.db import models

from django.forms import model_to_dict

from apps.erp.models import Clientes, Productos, Servicios
from apps.parametros.models import Modelos, Prioridades, Estados
from apps.usuarios.models import Usuarios


#   Clase Trabajos
class Trabajos(models.Model):
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario')
    fechaEntrada = models.DateField(verbose_name='Fecha de Entrada')
    fechaSalida = models.DateField(verbose_name='Fecha de Salida', blank=True, null=True)
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING, verbose_name='Cliente')
    modelo = models.ForeignKey(Modelos, models.DO_NOTHING, verbose_name='Modelo')
    usuarioAsignado = models.ForeignKey(Usuarios, models.DO_NOTHING, related_name='usuarioAsignado',
                                        verbose_name='Usuario Asignado', blank=True, null=True)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    percepcion = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    prioridad = models.ForeignKey(Prioridades, models.DO_NOTHING, verbose_name='Prioridad', blank=True, null=True)
    estados = (
        ('PENDIENTE', 'PENDIENTE'),
        ('PLANIFICADO', 'PLANIFICADO'),
        ('PROCESO', 'EN PROCESO'),
        ('FINALIZADO', 'FINALIZADO'),
        ('ENTREGADO', 'ENTREGADO'),
        ('CANCELADO', 'CANCELADO'),
    )
    estadoTrabajo = models.CharField(max_length=11, choices=estados, default='PENDIENTE')
    fichaTrabajo = models.CharField(max_length=20, verbose_name='Ficha de Trabajo Asociada', blank=True, null=True)
    observaciones = models.CharField(max_length=100, verbose_name='Observaciones', blank=True, null=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} - {} - {} - {}'.format(self.id, self.modelo.marca.nombre, self.modelo.nombre,
                                          self.cliente.razonSocial)

    def toJSON(self):
        item = model_to_dict(self)
        item['usuario'] = self.usuario.toJSON()
        try:
            item['usuarioAsignado'] = self.usuarioAsignado.toJSON()
        except:
            pass
        item['cliente'] = self.cliente.toJSON()
        item['modelo'] = self.modelo.toJSON()
        try:
            item['prioridad'] = self.prioridad.toJSON()
        except:
            pass
        return item

    class Meta:
        verbose_name = 'Trabajo'
        verbose_name_plural = 'Trabajos'
        db_table = 'trabajos'
        ordering = ['id']

        # Para convertir a MAYUSCULA

    def save(self, force_insert=False, force_update=False):
        try:
            self.fichaTrabajo = self.fichaTrabajo.upper()
        except:
            pass
        try:
            self.observaciones = self.observaciones.upper()
        except:
            pass
        super(Trabajos, self).save(force_insert, force_update)


# Detalle de Productos del Trabajo
class DetalleProductosTrabajo(models.Model):
    trabajo = models.ForeignKey(Trabajos, models.DO_NOTHING)
    producto = models.ForeignKey(Productos, models.DO_NOTHING)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    observaciones = models.CharField(max_length=100, verbose_name='Observaciones', blank=True, null=True)
    estado = models.BooleanField(default=False)
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario', blank=True, null=True)
    fechaDetalle = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.producto.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['trabajo'])
        item['producto'] = self.producto.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Productos - Trabajo'
        verbose_name_plural = 'Detalle de Productos - Trabajos'
        db_table = 'trabajos_detalle_productos'
        ordering = ['id']

    def save(self, force_insert=False, force_update=False):
        try:
            self.observaciones = self.observaciones.upper()
        except:
            pass
        super(DetalleProductosTrabajo, self).save(force_insert, force_update)


# Detalle de Servicios del Trabajo
class DetalleServiciosTrabajo(models.Model):
    trabajo = models.ForeignKey(Trabajos, models.DO_NOTHING)
    servicio = models.ForeignKey(Servicios, models.DO_NOTHING)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    observaciones = models.CharField(max_length=100, verbose_name='Observaciones', blank=True, null=True)
    estado = models.BooleanField(default=False)
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario', blank=True, null=True)
    fechaDetalle = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.servicio.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['trabajo'])
        item['servicio'] = self.servicio.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Servicios - Trabajo'
        verbose_name_plural = 'Detalle de Servicios - Trabajos'
        db_table = 'trabajos_detalle_servicios'
        ordering = ['id']

    def save(self, force_insert=False, force_update=False):
        try:
            self.observaciones = self.observaciones.upper()
        except:
            pass
        super(DetalleServiciosTrabajo, self).save(force_insert, force_update)
