from django.db import models
from simple_history.models import HistoricalRecords

from apps.usuarios.models import Usuarios
from django.forms import model_to_dict

class notificacionesGenerales(models.Model):
	fechaNotificacion = models.DateTimeField()
	ESTADO = (('pendiente', 'Pendiente'),
	          ('vista', 'Vista'),
	          ('urgente', 'Urgente'))
	estado = models.CharField(max_length=9, choices=ESTADO, blank=True)
	titulo = models.CharField(max_length=30)
	descripcion = models.CharField(max_length=254)
	enviadoAUser = models.ForeignKey(Usuarios, models.DO_NOTHING, verbose_name='Usuario al que se le envió la notif')
	fechaRevisionUser = models.DateTimeField(blank=True, null=True)
	history = HistoricalRecords()

	def toJSON(self):
		item = model_to_dict(self)
		return item

	def __str__(self):
		return self.estado + self.titulo

	class Meta:
		verbose_name = 'Notificación genérica'
		verbose_name_plural = 'Notificaciones Genéricas'
		db_table = 'notif_notif_generica'
		ordering = ['fechaNotificacion']