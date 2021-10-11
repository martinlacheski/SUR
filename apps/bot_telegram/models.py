import datetime
from django.db import models
from apps.erp.models import Clientes
from apps.usuarios.models import Usuarios
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



# Usuarios a los cuales se les notificó el incidente. (capaz no haga falta)
class notificacionUsuarios_Tel(models.Model):
    usuario_id = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario notificado')
    registro_id = models.ForeignKey(registroBotIncidencias, models.DO_NOTHING, verbose_name='registro log asociado')

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

# Create your models here.
