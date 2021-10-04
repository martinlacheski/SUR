from django.db import models
from django.forms import model_to_dict

from apps.erp.models import Productos, Servicios, Clientes
from apps.parametros.models import Modelos


#   Clase PresupuestoBase
from apps.usuarios.models import Usuarios


class PlantillaPresupuestos(models.Model):
    modelo = models.ForeignKey(Modelos, models.DO_NOTHING, verbose_name='Modelo')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', unique=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} - {} - {}'.format(self.modelo.marca.nombre, self.modelo.nombre, self.descripcion)

    def toJSON(self):
        item = model_to_dict(self)
        item['modelo'] = self.modelo.toJSON()
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        unique_together = ['modelo', 'descripcion']
        verbose_name = 'Plantilla de Presupuesto'
        verbose_name_plural = 'Plantillas de Presupuestos'
        db_table = 'presupuestos_plantilla'
        ordering = ['id']

        # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        try:
            self.descripcion = self.descripcion.upper()
        except:
            pass
        super(PlantillaPresupuestos, self).save(force_insert, force_update)


# Detalle de Productos del Presupuesto Base
class DetalleProductosPlantillaPresupuesto(models.Model):
    presupuestoPlantilla = models.ForeignKey(PlantillaPresupuestos, models.DO_NOTHING)
    producto = models.ForeignKey(Productos, models.DO_NOTHING)
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return self.producto.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['presupuestoPlantilla'])
        item['producto'] = self.producto.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle de Productos - Plantilla Presupuesto'
        verbose_name_plural = 'Detalle de Productos - Plantilla de Presupuesto'
        db_table = 'presupuestos_plantilla_detalle_productos'
        ordering = ['id']


# Detalle de Servicios del Presupuesto Base
class DetalleServiciosPlantillaPresupuesto(models.Model):
    presupuestoPlantilla = models.ForeignKey(PlantillaPresupuestos, models.DO_NOTHING)
    servicio = models.ForeignKey(Servicios, models.DO_NOTHING)
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return self.servicio.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['presupuestoPlantilla'])
        item['servicio'] = self.servicio.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle de Servicios - Plantilla Presupuesto'
        verbose_name_plural = 'Detalle de Servicios - Plantilla Presupuesto'
        db_table = 'presupuestos_plantilla_detalle_servicios'
        ordering = ['id']


#   Clase Presupuestos
class Presupuestos(models.Model):
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario')
    fecha = models.DateField(verbose_name='Fecha')
    validez = models.PositiveIntegerField(default=1,verbose_name='Validez del Presupuesto')
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING, verbose_name='Cliente')
    modelo = models.ForeignKey(Modelos, models.DO_NOTHING, verbose_name='Modelo')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    percepcion = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.BooleanField(default="", blank=True, null=True)
    observaciones = models.CharField(max_length=100, verbose_name='Observaciones', blank=True, null=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} - {} - {} - {}'.format(self.fecha, self.modelo.marca.nombre, self.modelo.nombre, self.cliente.razonSocial)

    def toJSON(self):
        item = model_to_dict(self)
        item['usuario'] = self.usuario.toJSON()
        item['cliente'] = self.cliente.toJSON()
        item['modelo'] = self.modelo.toJSON()
        return item

    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        db_table = 'presupuestos'
        ordering = ['id']

        # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        try:
            self.observaciones = self.observaciones.upper()
        except:
            pass
        super(Presupuestos, self).save(force_insert, force_update)


# Detalle de Productos del Presupuesto
class DetalleProductosPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuestos, models.DO_NOTHING)
    producto = models.ForeignKey(Productos, models.DO_NOTHING)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.producto.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['presupuesto'])
        item['producto'] = self.producto.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Productos - Presupuesto'
        verbose_name_plural = 'Detalle de Productos - Presupuestos'
        db_table = 'presupuestos_detalle_productos'
        ordering = ['id']


# Detalle de Servicios del Presupuesto
class DetalleServiciosPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuestos, models.DO_NOTHING)
    servicio = models.ForeignKey(Servicios, models.DO_NOTHING)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.servicio.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['presupuesto'])
        item['servicio'] = self.servicio.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Servicios - Presupuesto'
        verbose_name_plural = 'Detalle de Servicios - Presupuestos'
        db_table = 'presupuestos_detalle_servicios'
        ordering = ['id']