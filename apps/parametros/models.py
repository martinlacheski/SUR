from django.db import models
from django.forms import model_to_dict


class TiposIVA(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Tipo de IVA', unique=True)
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
    nombre = models.CharField(max_length=100, verbose_name='Condición frente al IVA', unique=True)

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
    nombre = models.CharField(max_length=100, verbose_name='Condición de Pago', unique=True)

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