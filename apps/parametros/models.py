from django.db import models
from django.forms import model_to_dict

from apps.geografico.models import Localidades
from config.settings import MEDIA_URL, STATIC_URL


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


class TiposPercepciones(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    percepcion = models.DecimalField(default=0, max_digits=9, decimal_places=2, verbose_name='Porcentaje')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Percepción'
        verbose_name_plural = 'Tipos de Percepciones'
        db_table = 'parametros_tipos_percepciones'
        ordering = ['id']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(TiposPercepciones, self).save(force_insert, force_update)


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


class MediosPago(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Medio de Pago'
        verbose_name_plural = 'Medios de Pagos'
        db_table = 'parametros_medios_pagos'
        ordering = ['id']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(MediosPago, self).save(force_insert, force_update)


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
    orden = models.PositiveIntegerField(default=0)

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
    plazoPrioridad = models.PositiveIntegerField(default=0, verbose_name='Días de PLazo')

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


class Empresa(models.Model):
    razonSocial = models.CharField(max_length=100, verbose_name='Razón Social')
    condicionIVA = models.ForeignKey(CondicionesIVA, models.DO_NOTHING, verbose_name='Condición frente al IVA')
    cuit = models.CharField(max_length=13, verbose_name='Cuit', unique=True)
    localidad = models.ForeignKey(Localidades, models.DO_NOTHING, verbose_name='Localidad')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    telefono = models.CharField(max_length=100, verbose_name='Teléfono')
    email = models.EmailField(max_length=254, verbose_name='Dirección de correo electrónico')
    passwordEmail = models.CharField(max_length=128, null=True, blank=True)
    botTelegram = models.CharField(max_length=100, verbose_name='Bot Telegram', null=True, blank=True)
    tokenTelegram = models.CharField(max_length=100, verbose_name='Token Telegram', null=True, blank=True)
    facebook = models.CharField(max_length=100, verbose_name='Cuenta de Facebook', null=True, blank=True)
    instagram = models.CharField(max_length=100, verbose_name='Cuenta de Instagram', null=True, blank=True)
    paginaWeb = models.CharField(max_length=100, verbose_name='Dirección de Página Web', null=True, blank=True)
    imagen = models.ImageField(upload_to='empresas/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    cbu = models.CharField(max_length=22, verbose_name='Clave CBU/CVU', null=True, blank=True)
    alias = models.CharField(max_length=100, verbose_name='Alias', null=True, blank=True)
    nroCuenta = models.CharField(max_length=100, verbose_name='Número de Cuenta', null=True, blank=True)

    def __str__(self):
        return self.razonSocial

    def toJSON(self):
        item = model_to_dict(self)
        item['imagen'] = self.get_imagen()
        return item

    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Datos Empresa'
        db_table = 'parametros_empresa'

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.razonSocial = self.razonSocial.upper()
        self.direccion = self.direccion.upper()
        try:
            self.alias = self.alias.upper()
        except:
            pass
        super(Empresa, self).save(force_insert, force_update)