from django.db import models
from django.forms import model_to_dict


class TiposIVA(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    iva = models.DecimalField(default=21, max_digits=9, decimal_places=2, verbose_name='Porcentaje')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de IVA'
        verbose_name_plural = 'Tipos de IVA'
        db_table = 'parametros_tipos_iva'
        ordering = ['id']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(TiposIVA, self).save(force_insert, force_update)


class CondicionesIVA(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Condición frente al IVA'
        verbose_name_plural = 'Condiciones frente al IVA'
        db_table = 'parametros_condiciones_iva'
        ordering = ['id']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(CondicionesIVA, self).save(force_insert, force_update)


class CondicionesPago(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Condición de Pago'
        verbose_name_plural = 'Condiciones de Pagos'
        db_table = 'parametros_condiciones_pagos'
        ordering = ['id']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(CondicionesPago, self).save(force_insert, force_update)


class TiposComprobantes(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Comprobante'
        verbose_name_plural = 'Tipos de Comprobantes'
        db_table = 'parametros_tipos_comprobantes'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(TiposComprobantes, self).save(force_insert, force_update)


class Marcas(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        db_table = 'parametros_marcas'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(Marcas, self).save(force_insert, force_update)


class Modelos(models.Model):
    marca = models.ForeignKey(Marcas, models.DO_NOTHING, verbose_name='Marca')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.CharField(max_length=254, verbose_name='Descripcion', null=True, blank=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['marca'] = self.marca.toJSON()
        return item

    class Meta:
        unique_together = ['marca', 'nombre']
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        db_table = 'parametros_modelos'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        try:
            self.descripcion = self.descripcion.upper()
        except:
            pass
        super(Modelos, self).save(force_insert, force_update)

#Estados de TRABAJOS
class Estados(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Estado Trabajo'
        verbose_name_plural = 'Estados Trabajos'
        db_table = 'parametros_estados_trabajos'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(Estados, self).save(force_insert, force_update)

#Prioridad de TRABAJOS
class Prioridades(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Prioridad de Trabajo'
        verbose_name_plural = 'Prioridades de Trabajos'
        db_table = 'parametros_prioridades_trabajos'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(Prioridades, self).save(force_insert, force_update)