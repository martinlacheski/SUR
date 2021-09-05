from django.db import models
from django.forms import model_to_dict


class TiposIVA(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Tipo de IVA', unique=True)
    iva = models.DecimalField(default=0.21, max_digits=9, decimal_places=3, verbose_name='Porcentaje')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de IVA'
        verbose_name_plural = 'Tipos de IVA'
        db_table = 'parametros_iva'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
       self.nombre = self.nombre.upper()
       super(TiposIVA, self).save(force_insert, force_update)
