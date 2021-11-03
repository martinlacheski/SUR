from django.conf import settings
import telegram
from apps.trabajos.models import Trabajos
from apps.bot_telegram.models import seguimientoTrabajos
from apps.bot_telegram.logicaBot import porcentajeTrabajo
from apps.parametros.models import EstadoParametros
from django.core.exceptions import ObjectDoesNotExist
from apscheduler.schedulers.background import BackgroundScheduler
import datetime


bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')


def rastreoTrabajos():
	# Buscamos trabajos que no estén en ninguno de estos estados.
	estados = EstadoParametros.objects.last()
	estados_excluidos = [estados.estadoFinalizado.id,
	                     estados.estadoEntregado.id,
	                     estados.estadoCancelado.id]
	trabajos = Trabajos.objects.exclude(estadoTrabajo__in=estados_excluidos)

	# Por cada uno de ellos decidimos si creamos un job o no
	for t in trabajos:
		avance = porcentajeTrabajo(t)
		bot.send_message(chat_id=630659758, text=str(avance))
		cant_dias_en_proceso = datetime.date.today() - t.fechaEntrada
		# Si la cantidad de días desde que el trabajo está en la empresa es mayor a su plazo aproximado, hacemos cosas
		if cant_dias_en_proceso.days > t.prioridad.plazoPrioridad:
			try:
				# Si ya existe un seguimiento para el trabajo en cuestión, ponemos su cant notif a 0
				segTrab = seguimientoTrabajos.objects.get(trabajo=t)
				segTrab.cantVecesNotif = 0
			except ObjectDoesNotExist:
				# Si no existe, creamos un seguimiento
				segTrab = seguimientoTrabajos()
				segTrab.trabajo = t
				segTrab.inicialUserAsig = t.usuarioAsignado
				segTrab.ultPorcentajeAvance = float(avance)
				segTrab.cantVecesNotif = 0
				segTrab.save()
			bot.send_message(chat_id=630659758, text="creo job")
			crearJob(t, segTrab)
			

			# Si no hay avance en el trabajo
			if float(avance) != 100:
				print("Enviar msj")
				print("Programar job a la espera de en 1h")


# def job(trabajo, seguimiento):
# 	bot.send_message(chat_id=630659758, text=str(trabajo))
# 	bot.send_message(chat_id=630659758, text=str(seguimiento))
	# Si el usuario aún no respondió
	"""
	if not seguimiento.respuestaUser:
		if segTrab.cantVecesNotif <= 3:
			bot.send_message(chat_id=630659758, text="notifico usuario sobre el trabajo")
			segTrab.cantVecesNotif += 1
			segTrab.save()
		if segTrab.cantVecesNotif > 3:
			bot.send_message(chat_id=630659758, text="le digo al usuario actual que su trabajo fué reasignado")
			bot.send_message(chat_id=630659758, text="decido a qué usuario voy a asignar")
			bot.send_message(chat_id=630659758, text="le digo al nuevo user que tiene un nuevo trabajo")
			bot.send_message(chat_id=630659758, text="le aviso a administración sobre el acontecimiento")
	# En caso de que ya haya respuesta
	else:
	"""	

			








# Se encarga de crear los jobs. Nada más. El job decide qué datos alterar y qué decisiones tomar
def crearJob(trabajo, seguimiento):
	scheduler_eventos = BackgroundScheduler(timezone=settings.TIME_ZONE)
	start_date = datetime.datetime.today()
	end_date = datetime.datetime.today() + datetime.timedelta(hours=3)
	scheduler_eventos.add_job(job, 'interval', hours=1, start_date=start_date, end_date=end_date, args=[trabajo, seguimiento])
	scheduler_eventos.start()









def mensaje(trabajo):
	usuarioAsig = trabajo.usuarioAsignado.chatIdUsuario
	mensaje = "Hola! Te informo que el trabajo Nro°" + str(trabajo.id) +\
	          " no tiene avances según la prioridad establecida "

	# if trabajo.observaciones:
	# 	mensaje += "📝 Algunas observaciones son: " + str(trabajo.observaciones) + "\n\n"
	# mensaje += "💰 El importe a abonar es: $" + str(trabajo.total) + " pesos.\n\n"
	# mensaje += "Te pido que indiques cuándo lo vas a pasar a buscar presionando cualquiera de los siguiente botones."
	# bot.send_message(chat_id=cliente.chatIdCliente, text=mensaje)
	#
	# # Callback data
	# data_hoy = {'hoy': str(datetime.date.today()), 'cliente': str(cliente.id), 'trabajo': str(trabajo.id),
	#
	#             }
	# sig_habil = {'sig_dia_habil': str(dia_habil_siguiente(datetime.date.today())), 'cliente': str(cliente.id),
	#              'trabajo': str(trabajo.id),
	#
	#              }
	# se_comunica = {'se_secomunica': 'Se comunicará luego.'}
	# keyboard = [[InlineKeyboardButton("Hoy", callback_data=str(data_hoy))],
	#             [InlineKeyboardButton("Siguiente día hábil", callback_data=str(sig_habil))],
	#             [InlineKeyboardButton("Me comunico luego", callback_data=str(se_comunica))], ]
	# reply_markup = InlineKeyboardMarkup(keyboard)
	# bot.send_message(chat_id=cliente.chatIdCliente, text="Opciones:\n", reply_markup=reply_markup)

