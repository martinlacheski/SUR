from django.db import models
from django.forms import model_to_dict


class Categorias(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    abreviatura = models.CharField(max_length=20, verbose_name='Abreviatura')

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
