import datetime
from django.db import models
from apps.erp.models import Clientes
from apps.usuarios.models import Usuarios
from apps.trabajos.models import Trabajos
from django.forms import model_to_dict

class registroBotIncidencias (models.Model):
    fechaSuceso = models.DateTimeField(default=datetime.datetime.today())
    observacion = models.TextField(blank=True, null=True)
    revisadoPor = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario que revisó el inconveniente',
                                    blank=True, null=True)
    fechaRevision = models.DateTimeField(default=datetime.datetime.today(), blank=True, null=True)

    class Meta:
        verbose_name = 'Registro no Exitoso de Cliente'
        verbose_name_plural = 'Registros no Exitosos de Clientes'
        db_table = 'bot_log_incidencias'
        ordering = ['fechaSuceso']



# Usuarios a los cuales se les notificó el incidente. (no está en funcionamiento. La dejo por las dudas 12/10/2021)
class notificacionUsuarios_Tel(models.Model):
    usuario_id = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario notificado')
    registro_id = models.ForeignKey(registroBotIncidencias, models.DO_NOTHING, verbose_name='registro log asociado')

# Registra a qué usuarios le vamos a notificar sobre incidencias.
class notifIncidentesUsuarios(models.Model):
    usuario_id = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario a notificar')

    class Meta:
        verbose_name = 'Notificacion de incidencia'
        verbose_name_plural = 'Notificaciones de incidencia'
        db_table = 'usuarios_notifIncidencias'
        ordering = ['usuario_id']

    def toJSON(self):
        item = model_to_dict(self)
        item['usuario_id'] = self.usuario_id.toJSON()
        return item

class respuestaTrabajoFinalizado(models.Model):
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING, verbose_name='Cliente que respondió')
    trabajo = models.ForeignKey(Trabajos, models.DO_NOTHING, verbose_name='Trabajo asociado')
    fechaRespuesta = models.DateTimeField(default=datetime.datetime.today(), blank=True, null=True)
    respuesta_puntual = models.DateField(blank=True, null=True)
    respuesta_generica = models.CharField(max_length=20, verbose_name='Respuesta', null=True, blank=True)

    class Meta:
        verbose_name = 'Respuesta de trabajo finalizado'
        verbose_name_plural = 'Respuestas de trabajo finalizado'
        db_table = 'bot_respuestaTrabajoFinalziado'
        ordering = ['fechaRespuesta']



class seguimientoTrabajos(models.Model):
    trabajo = models.ForeignKey(Trabajos, models.DO_NOTHING, verbose_name='Trabajo asociado')
    # ultPorcentajeAvance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cantVecesNotif_dia = models.IntegerField(default=0, verbose_name="Cantidad de veces notificadas en el día")
    cantVecesNotif_total = models.IntegerField(default=0, verbose_name="Cantidad de veces TOTALES notificadas (1 por día)")
    inicialUserAsig = models.ForeignKey(Usuarios, models.DO_NOTHING,
                                        verbose_name='Inicial. Usuario asociado',
                                        related_name="Usuario_inicial",
                                        null=True, blank=True)
    ultUserAsig = models.ForeignKey(Usuarios, models.DO_NOTHING,
                                    verbose_name='Ult. Usuario asociado',
                                    blank=True, null=True, related_name="Usuario_final")
    respuestaUser = models.CharField(max_length=40, verbose_name='Respuesta', null=True, blank=True)
    fechaEnvio = models.DateTimeField(default=datetime.datetime.today(), null=True, blank=True)
    fechaRespuesta = models.DateTimeField(blank=True, null=True)
    notif_por_sist = models.IntegerField(default=0, verbose_name="Cantidad de veces notificadas por Sistema.")

    class Meta:
        verbose_name = 'Seguimiento de estado de trabajo'
        verbose_name_plural = 'Seguimiento de estado de trabajos'
        db_table = 'bot_seguimientoTrabajos'
        ordering = ['trabajo']