from builtins import chr

from django.db import models

from django.forms import model_to_dict


class Paises(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    #estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        db_table = 'paises'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(Paises, self).save(force_insert, force_update)


class Provincias(models.Model):
    pais = models.ForeignKey(Paises, models.DO_NOTHING, verbose_name='Pais')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    #estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['pais'] = self.pais.toJSON()
        return item

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        db_table = 'provincias'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(Provincias, self).save(force_insert, force_update)


class Localidades(models.Model):
    pais = models.ForeignKey(Paises, models.DO_NOTHING, verbose_name='Pais')
    provincia = models.ForeignKey(Provincias, models.DO_NOTHING, verbose_name='Provincia')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    codigo_postal = models.CharField(max_length=10, verbose_name='Código Postal')
    #estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['provincia'] = self.provincia.toJSON()
        item['pais'] = self.pais.toJSON()
        return item

    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
        db_table = 'localidades'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        self.codigo_postal = self.codigo_postal.upper()
        super(Localidades, self).save(force_insert, force_update)
