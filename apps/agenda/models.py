from django.db import models
from django.forms import model_to_dict
from django.utils import timezone
from apps.usuarios.models import Usuarios

class tiposEvento(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    horarioRecordatorio = models.TimeField() # Avisar a esta hora
    recordarSistema = models.BooleanField(default=True) # Si le va a aparecer alguna notificacion
    recordarTelegram = models.BooleanField() # Si se le va a enviar un msj al telegram


    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        # item['usuarioNotif'] = self.usuarioNotif.toJSON()
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
        return

class eventosAgenda(models.Model):
    fechaCreacion = models.DateField(default=timezone.now)
    tipoEvento = models.ForeignKey(tiposEvento, models.DO_NOTHING, verbose_name='tipoEvento')
    fechaNotificacion = models.DateField()
    fechaFinalizacion = models.DateField(blank=True, null=True)
    ultimaNotificacionSist = models.DateField(blank=True, null=True)            # última vez que el usuario confirmó que vió la notif (sist)
    ultimaNotificacionTel = models.DateField(blank=True, null=True)             # última vez que el usuario confirmó que vió la notif (tel)
    ultimaVistaNotifiSist = models.DateField(blank=True, null=True)             # utlima vez avisada por el sist
    ultimaVistaNotifiTel = models.DateField(blank=True, null=True)              # ultima vez avisada por tel
    descripcion = models.TextField()
    cantNotifTelegram = models.IntegerField(default=0, verbose_name='cantidad de veces notificadas', blank=True)
    cantNotifSistema = models.IntegerField(default=0, verbose_name='cantidad de veces notificadas')
    vencido = models.BooleanField(default=False)
    resuelto = models.BooleanField(default=False)
    REPETICION = (
        ('daily', 'Diariamente'),
        ('weekly', 'Semanalmente'),
        ('monthly', 'Mensualmente'),
    )
    repeticion = models.CharField(max_length=7, choices=REPETICION, blank=True)

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


class diasAvisoEvento(models.Model):
    diasAntelacion = models.PositiveIntegerField(default=0)
    lunes = models.BooleanField(default=True)
    martes = models.BooleanField(default=True)
    miercoles = models.BooleanField(default=True)
    jueves = models.BooleanField(default=True)
    viernes = models.BooleanField(default=True)
    sabado = models.BooleanField(default=False)
    domingo = models.BooleanField(default=False)

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = 'Dias a recordar'
        verbose_name_plural = 'Dias a recordar'
        db_table = 'agenda_diasAvisoEvento'
        ordering = ['diasAntelacion']


class notificacionUsuarios (models.Model):
    tipoEvento = models.ForeignKey(tiposEvento, models.DO_NOTHING, verbose_name='tipoEvento')
    usuarioNotif = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='UsuarioAsoc', null=False, blank=False)


    def toJSON(self):
        item = model_to_dict(self)
        item['usuarioNotif'] = self.usuarioNotif.toJSON()
        item['tipoEvento'] = self.tipoEvento.toJSON()
        return item

    class Meta:
        verbose_name = 'Notificacion Usuarios'
        verbose_name_plural = 'Notificacion Usuarios'
        db_table = 'agenda_notificacionUsuarios'
        ordering = ['tipoEvento']
