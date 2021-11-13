from django.db import models
from simple_history.models import HistoricalRecords

from apps.erp.models import Clientes
from apps.usuarios.models import Usuarios
from apps.trabajos.models import Trabajos
from django.forms import model_to_dict



# Registra a qué usuarios administrativos le vamos a notificar eventos en el bot.
class notifUsuariosBot(models.Model):
    usuario_id = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario a notificar')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Notificacion de incidencia'
        verbose_name_plural = 'Notificaciones de incidencia'
        db_table = 'bot_usuarios_a_notificar'
        ordering = ['usuario_id']

    def toJSON(self):
        item = model_to_dict(self)
        item['usuario_id'] = self.usuario_id.toJSON()
        return item

class respuestaTrabajoFinalizado(models.Model):
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING, verbose_name='Cliente que respondió')
    trabajo = models.ForeignKey(Trabajos, models.DO_NOTHING, verbose_name='Trabajo asociado')
    fechaRespuesta = models.DateTimeField(blank=True, null=True)
    respuesta_puntual = models.DateField(blank=True, null=True)
    respuesta_generica = models.CharField(max_length=20, verbose_name='Respuesta', null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Respuesta de trabajo finalizado'
        verbose_name_plural = 'Respuestas de trabajo finalizado'
        db_table = 'bot_respuestaTrabajoFinalziado'
        ordering = ['fechaRespuesta']



class seguimientoTrabajos(models.Model):
    trabajo = models.ForeignKey(Trabajos, models.DO_NOTHING, verbose_name='Trabajo asociado')
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
    fechaEnvio = models.DateTimeField(null=True, blank=True)
    fechaRespuesta = models.DateTimeField(blank=True, null=True)
    notif_por_sist = models.IntegerField(default=0, verbose_name="Cantidad de veces notificadas por Sistema.")
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Seguimiento de estado de trabajo'
        verbose_name_plural = 'Seguimiento de estado de trabajos'
        db_table = 'bot_seguimientoTrabajos'
        ordering = ['trabajo']