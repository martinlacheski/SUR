from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.forms import model_to_dict

from apps.geografico.models import Localidades

#   Clase Tipos de Usuarios
from config.settings import MEDIA_URL


class TiposUsuarios(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Usuario'
        verbose_name_plural = 'Tipos de Usuarios'
        db_table = 'usuarios_tipos'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(TiposUsuarios, self).save(force_insert, force_update)


#   Clase Usuarios
class Usuarios(AbstractUser):
    legajo = models.CharField(max_length=10, null=True, blank=True, verbose_name='Legajo')
    fechaIngreso = models.DateField(default=datetime.now, verbose_name='Fecha de Ingreso')
    cuil = models.CharField(max_length=15, verbose_name='Cuil', null=True, blank=True)
    localidad = models.ForeignKey(Localidades, models.DO_NOTHING, verbose_name='Localidad', null=True, blank=True)
    direccion = models.CharField(max_length=100, verbose_name='Dirección', null=True, blank=True)
    telefono = models.CharField(max_length=100, verbose_name='Teléfono', null=True, blank=True)
    tipoUsuario = models.ForeignKey(TiposUsuarios, models.DO_NOTHING, verbose_name='Tipo de Usuario', null=True,
                                    blank=True)
    imagen = models.ImageField(upload_to='usuarios/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login', 'date_joined', 'groups'])
        item['fechaingreso'] = self.fechaIngreso.strftime('%dd/%MM/%YYYY')
        item['full_name'] = self.get_full_name()
        item['imagen'] = self.get_imagen()
        # item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(MEDIA_URL, 'empty.png')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'usuarios'
        ordering = ['last_name', 'first_name']

    # Para convertir a MAYUSCULA
    def pre_save(self, force_insert=False, force_update=False):
        # def save(self, *args, **kwargs):
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        self.legajo = self.legajo.upper()
        self.direccion = self.direccion.upper()
        self.telefono = self.direccion.upper()
        super(Usuarios, self).save(force_insert, force_update)
    # super(Usuarios, self).save(*args, **kwargs)
