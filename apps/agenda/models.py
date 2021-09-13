from django.db import models
from django.forms import model_to_dict
from django.utils import timezone
from apps.usuarios.models import Usuarios

class tiposEvento(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    horarioRecordatorio = models.TimeField() # Avisar a esta hora
    recordarSistema = models.BooleanField(default=True) # Si le va a aparecer alguna notificacion
    recordarTelegram = models.BooleanField() # Si se le va a enviar un msj al telegram
    recordarEmail = models.BooleanField() # Si se le va a enviar un correo
    usuarioNotif = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='UsuarioAsoc', null=False, blank=False) #En este campo tienen que ir los usuarios. Se espera por integración de Martin


    #estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Evento'
        verbose_name_plural = 'Tipos de Eventos'
        db_table = 'agenda_tiposEventos'
        ordering = ['nombre']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(tiposEvento, self).save(force_insert, force_update)

class eventosAgenda(models.Model):
    fechaCreacion = models.DateField(default=timezone.now)
    tipoEvento = models.ForeignKey(tiposEvento, models.DO_NOTHING, verbose_name='tipoEvento')
    fechaNotificacion = models.DateField()
    descripcion = models.TextField()
    REPETICION = (
        ('DIA', 'Diariamente'),
        ('SEM', 'Semanalmente'),
        ('MEN', 'Mensualmente'),
    )
    repeticion = models.CharField(max_length=3, choices=REPETICION, blank=True)
    # estado = models.BooleanField(default=True)
#Para save en campo repeticion, se guarda así (es solo un ejemplo):
    # p = eventosAgenda(name="Fred Flintstone", repeticion="DIA")

    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Evento Agenda'
        verbose_name_plural = 'Eventos Agenda'
        db_table = 'agenda_eventosAgenda'
        ordering = ['fechaCreacion']

    # Para convertir a MAYUSCULA
    """
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(Paises, self).save(force_insert, force_update)
    """