from django.db import models
from django.forms import model_to_dict

class tiposEvento(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    tiempoRecordatorio = models.TimeField()
    recordarSistema = models.BooleanField(default=True)
    recordarWpp = models.BooleanField()
    recordarEmail = models.BooleanField()
    #estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Evento'
        verbose_name_plural = 'Tipos de Eventos'
        db_table = 'tiposEventos'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(tiposEvento, self).save(force_insert, force_update)

class eventosAgenda(models.Model):
    fechaCreacion = models.DateTimeField()
    tipoEvento = models.ForeignKey(tiposEvento, models.DO_NOTHING, verbose_name='tipoEvento')
    fechaNotificacion = models.DateTimeField()
    descripcion = models.TextField()
    #estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Evento Agenda'
        verbose_name_plural = 'Eventos Agenda'
        db_table = 'eventosAgenda'
        ordering = ['fechaCreacion']

    # Para convertir a MAYUSCULA
    """
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(Paises, self).save(force_insert, force_update)
    """