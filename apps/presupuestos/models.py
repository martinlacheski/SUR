from django.db import models
from django.forms import model_to_dict

from apps.erp.models import Productos, Servicios
from apps.parametros.models import Modelos


#   Clase PresupuestoBase
class PresupuestosBase(models.Model):
    modelo = models.ForeignKey(Modelos, models.DO_NOTHING, verbose_name='Modelo')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', unique=True)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} - {} - {}'.format(self.modelo.marca.nombre, self.modelo.nombre, self.descripcion)

    def toJSON(self):
        item = model_to_dict(self)
        item['modelo'] = self.modelo.toJSON()
        return item

    class Meta:
        unique_together = ['modelo', 'descripcion']
        verbose_name = 'Presupuesto Base'
        verbose_name_plural = 'Presupuestos Base'
        db_table = 'presupuesto_base'
        ordering = ['id']

        # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        try:
            self.descripcion = self.descripcion.upper()
        except:
            pass
        super(PresupuestosBase, self).save(force_insert, force_update)


# Detalle de Productos del Presupuesto Base
class DetalleProductosPresupuestoBase(models.Model):
    presupuestoBase = models.ForeignKey(PresupuestosBase, models.DO_NOTHING)
    producto = models.ForeignKey(Productos, models.DO_NOTHING)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.producto.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['presupuestoBase'])
        item['producto'] = self.producto.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Productos - Presupuesto Base'
        verbose_name_plural = 'Detalle de Productos - Presupuestos Base'
        ordering = ['id']


# Detalle de Servicios del Presupuesto Base
class DetalleServiciosPresupuestoBase(models.Model):
    presupuestoBase = models.ForeignKey(PresupuestosBase, models.DO_NOTHING)
    servicio = models.ForeignKey(Servicios, models.DO_NOTHING)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.servicio.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['presupuestoBase'])
        item['servicio'] = self.servicio.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Servicios - Presupuesto Base'
        verbose_name_plural = 'Detalle de Servicios - Presupuestos Base'
        ordering = ['id']
