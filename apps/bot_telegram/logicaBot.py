# Django y Python
import datetime
from apps.usuarios.models import Usuarios
from apps.erp.models import Clientes
from django.core.exceptions import *
from django.utils import timezone


# Proyecto
from apps.trabajos.models import *
from apps.bot_telegram.models import *
from apps.parametros.models import EstadoParametros
from apps.notif_channel.models import notificacionesGenerales
from apps.erp.models import Ventas, Compras, DetalleProductosVenta, DetalleServiciosVenta, DetalleProductosCompra
# Telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Socket
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import ast

# ***   CLIENTES ***

#   Chequea si el cliente ya registrado se quiere registrar como usuario. (no va a poder)
def check_chatid_user(chat_id):
    usuarios = Usuarios.objects.all()
    for user in usuarios:
        if user.chatIdUsuario == int(chat_id):
            return True
    return False

# Arma los mens
def mandarTrabajos(trabajosCliente):
    mensaje = "Actualmente tenés los siguientes trabajos en proceso:\n\n"
    for t in trabajosCliente:
        if checkEstado(t):  # Si el estado del trabajo es cualquiera menos Entregado, Cancelado
            mensaje += " ___ TRABAJO N° " + str(t.id) + "___\n"
            mensaje += "*️⃣  Marca: " + str(t.modelo.marca.nombre) + "\n"
            mensaje += "*️⃣️ Modelo: " + str(t.modelo.nombre) + "\n"
            mensaje += "📝 Observaciones: " + str(t.observaciones) + "\n"
            mensaje += "🛠️ Completado al : " + porcentajeTrabajo(t) + "%\n"
            mensaje += "\n\n"
    return mensaje

# Calcula porcentaje de realización de un trabajo concorde a su ponderación
def porcentajeTrabajo(trabajo):
    totalEsfuerzo = 0
    esfuerzoTrabRealizados = 0
    detalle = DetalleServiciosTrabajo.objects.filter(trabajo_id=trabajo.id)
    # Calculamos el total del esfuerzo del trabajo y lo dividimos por el total de esfuerzo de servicios ya realizados
    for d in detalle:
        totalEsfuerzo += d.servicio.esfuerzo
        if d.estado:
            esfuerzoTrabRealizados += d.servicio.esfuerzo
    if esfuerzoTrabRealizados == 0:
        porcentaje = 0
    else:
        porcentaje = esfuerzoTrabRealizados / totalEsfuerzo
    # Redondeamos para tener solo 2 decimales
    porcentaje = round(round(porcentaje, 2) * 100, 2)
    return str(porcentaje)

# Chequea estado del trabajo. No muestra los que fueron entregados o que se hayan cancelado.
def checkEstado(trabajo):
    estado = trabajo.estadoTrabajo_id
    trabajosParametros = EstadoParametros.objects.all()
    for parametros in trabajosParametros:
        if estado == parametros.estadoEspecial.id:
            return True
        elif estado == parametros.estadoInicial.id:
            return True
        elif estado == parametros.estadoPlanificado.id:
            return True
        elif estado == parametros.estadoFinalizado.id:
            return True
        else:
            return False

def dia_habil_siguiente(hoy):
    fecha_resultado = hoy
    if hoy.weekday() in range(4):
        fecha_resultado += datetime.timedelta(days=1)
    else:
        if hoy.weekday() == 4:
            fecha_resultado += datetime.timedelta(days=3)
        elif hoy.weekday() == 5:
            fecha_resultado += datetime.timedelta(days=2)
        elif hoy.weekday() == 6:
            fecha_resultado += datetime.timedelta(days=1)
    return fecha_resultado

#   Registra la respuesta del cliente respecto a cuándo va a buscar el trabajo finalizado.
#   Tambien genera respuestas tanto para clientes como para usuarios (telegram y sistema)

def registrarRetiro(respuesta):
    resp_to_dict = ast.literal_eval(respuesta)
    log_respuesta = respuestaTrabajoFinalizado()
    respuesta_bot = ""
    try:  # Estarán el trabajo y/o el cliente aún registrados?
        log_respuesta.trabajo = Trabajos.objects.get(pk=int(resp_to_dict['trabajo']))
        log_respuesta.cliente = Clientes.objects.get(pk=int(resp_to_dict['cliente']))
    except ObjectDoesNotExist:
        respuesta_bot = "❌ Ha ocurrido un problema. Probablemente tu trabajo o vos fueron dados de baja del sistema."
        return {'proc': False, 'respuesta_bot' : respuesta_bot}
    log_respuesta.fechaRespuesta = timezone.now().date()
    respuesta_bot = "Hola! 😌\nTe informo que el cliente " + str(log_respuesta.cliente) +" en respuesta a su trabajo" \
                                            " finalizado Nro° " + str(resp_to_dict['trabajo']) + ", informó que lo" \
                                            " pasará a buscar el día "
    respuesta_sist = "El cliente " + str(log_respuesta.cliente) +" en respuesta a su trabajo" \
                     " finalizado Nro° " + str(resp_to_dict['trabajo']) + ", informó que lo" \
                     " pasará a buscar el día "
    if 'hoy' in resp_to_dict:
        log_respuesta.respuesta_puntual = datetime.datetime.strptime(resp_to_dict['hoy'], '%Y-%m-%d').date()
        log_respuesta.respuesta_generica = "El cliente pasará a buscar el trabajo finalizado el día de hoy (" +\
                                            str(datetime.datetime.strptime(resp_to_dict['hoy'],
                                                                           '%Y-%m-%d').date().strftime('%d-%m-%Y')) +\
                                            "."
        respuesta_bot += str(datetime.datetime.strptime(resp_to_dict['hoy'], '%Y-%m-%d').date().strftime('%d-%m-%Y')) + "."
        respuesta_sist += str(datetime.datetime.strptime(resp_to_dict['hoy'], '%Y-%m-%d').date().strftime('%d-%m-%Y')) + "."
    elif 'sig_dia_habil' in resp_to_dict:
        log_respuesta.respuesta_puntual = datetime.datetime.strptime(resp_to_dict['sig_dia_habil'], '%Y-%m-%d').date()
        log_respuesta.respuesta_generica = "El cliente pasará a buscar el trabajo finalizado el día " + \
                                           str(datetime.datetime.strptime(resp_to_dict['sig_dia_habil'],
                                                                          '%Y-%m-%d').date().strftime('%d-%m-%Y')) + \
                                           "."
        respuesta_bot += str(datetime.datetime.strptime(resp_to_dict['sig_dia_habil'], '%Y-%m-%d').date().strftime('%d-%m-%Y')) + "."
        respuesta_sist += str(datetime.datetime.strptime(resp_to_dict['sig_dia_habil'], '%Y-%m-%d').date().strftime('%d-%m-%Y')) + "."
    elif 'se_secomunica' in resp_to_dict:
        log_respuesta.respuesta_generica = "El cliente se comunicará personalmente."
        respuesta_bot = "Hola! 😌\nTe informo que el cliente " + str(log_respuesta.cliente) +", en respuesta a su trabajo" \
                                           " finalizado Nro° " + str(resp_to_dict['trabajo']) + ", informó que" \
                                           " se comunicará personalmente para retirar dicho trabajo."
        respuesta_sist = "El cliente " + str(log_respuesta.cliente) +", en respuesta a su trabajo" \
                                           " finalizado Nro° " + str(resp_to_dict['trabajo']) + ", informó que" \
                                           " se comunicará personalmente para retirar dicho trabajo."
    log_respuesta.save()
    return {'proc': True, 'respuesta_bot': respuesta_bot, 'respuesta_sist' : respuesta_sist}


# ***   USUARIOS ***

#   Chequea si el usuario ya registrado se quiere registrar como cliente. (no va a poder)
def check_chatid_cliente(chat_id):
    clientes = Clientes.objects.all()
    for cliente in clientes:
        if cliente.chatIdCliente == int(chat_id):
            return True
    return False


def notificarSistema(titulo, descripcion):
    # TO-DO: acá se recorrería un for en alguna tabla en donde se setearon quienes reciben este tipo de notificaciones
    user = Usuarios.objects.get(pk=3)

    n = notificacionesGenerales()
    n.fechaNotificacion = timezone.now().date()
    n.estado = 'pendiente'
    n.titulo = titulo
    n.descripcion = descripcion
    n.enviadoAUser = user
    n.save()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('telegram_group', {"type": "receive",
                                                               "titulo": titulo,
                                                               "id_notif": str(n.id)})

def armarBotonesConsulta():
    keyboard = [
        [InlineKeyboardButton("⬆ Ventas del día", callback_data="ventasDia")],
        [InlineKeyboardButton("⬇ Compras del día", callback_data="comprasDia")],
        [InlineKeyboardButton("📅 Estado trabajos planif.", callback_data="trabajosPlanif")],
        [InlineKeyboardButton("🛠 Nuevos trabajos", callback_data="trabajosDia")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def generarReporte(eleccion):
    reporteDet = {}
    totalServicios = 0
    totalProductos = 0
    if eleccion == 'ventasDia':
        ventas = Ventas.objects.filter(fecha=timezone.now().date())
        cantVentas = 0
        for v in ventas:
            cantVentas += 1
            detVentaServicios = DetalleServiciosVenta.objects.filter(venta=v)
            detVentaProductos = DetalleProductosVenta.objects.filter(venta=v)
            for detS in detVentaServicios:
                totalServicios += detS.subtotal
            for detP in  detVentaProductos:
                totalProductos += detP.subtotal
        reporteDet['totalDia'] = totalProductos + totalServicios
        reporteDet['totalProductos'] = totalProductos
        reporteDet['totalServicios'] = totalServicios
        reporteDet['cantVentas'] = cantVentas
        reporteDet['tipo'] = "venta"
        return reporteDet

    if eleccion == 'comprasDia':
        compras = Compras.objects.filter(fecha=timezone.now().date())
        cantCompras = 0
        total = 0
        for c in compras:
            cantCompras +=1
            detCompraProductos = DetalleProductosCompra.objects.filter(compra=c)
            for detP in detCompraProductos:
                total += detP.subtotal
        reporteDet['totalDia'] = total
        reporteDet['totalProductos'] = total
        reporteDet['cantCompras'] = cantCompras
        reporteDet['tipo'] = "compra"
        return reporteDet

    if eleccion == 'trabajosPlanif':
        mensaje = ""
        ultPlanificacion = PlanificacionesSemanales.objects.latest('id')
        detPlanificacion = DetallePlanificacionesSemanales.objects.filter(planificacion=ultPlanificacion)
        if detPlanificacion:
            for det in detPlanificacion:
                mensaje += " ___ TRABAJO N° " + str(det.trabajo.id) + "___\n"
                mensaje += "*️⃣  Marca: " + str(det.trabajo.modelo.marca.nombre) + "\n"
                mensaje += "*️⃣️ Modelo: " + str(det.trabajo.modelo.nombre) + "\n"
                mensaje += "📝 Observaciones: " + str(det.trabajo.observaciones) + "\n"
                mensaje += "🛠️ Completado al : " + porcentajeTrabajo(det.trabajo) + "%\n"
                mensaje += "\n\n"
        else:
            mensaje += "Aún no hay trabajos en esta planificación!"

        reporteDet['mensaje'] = mensaje
        reporteDet['planifDesde'] = str(ultPlanificacion.fechaInicio.strftime('%d-%m-%Y'))
        reporteDet['planifHasta'] = str(ultPlanificacion.fechaFin.strftime('%d-%m-%Y'))
        reporteDet['tipo'] = "trabajosPlanif"
        return reporteDet

    if eleccion == 'trabajosDia':
        mensaje = ""
        trabajos = Trabajos.objects.filter(fechaEntrada=timezone.now().date())
        if trabajos:
            for t in trabajos:
                mensaje += " ___ TRABAJO N° " + str(t.id) + "___\n"
                mensaje += "*️⃣  Marca: " + str(t.modelo.marca.nombre) + "\n"
                mensaje += "*️⃣️ Modelo: " + str(t.modelo.nombre) + "\n"
                mensaje += "📝 Observaciones: " + str(t.observaciones) + "\n"
                mensaje += "🛠️ Completado al : " + porcentajeTrabajo(t) + "%\n"
                mensaje += "\n\n"
        else:
            mensaje += "Aún no han ingresado nuevos trabajos el día de hoy!"
        reporteDet['mensaje'] = mensaje
        reporteDet['tipo'] = "trabajosDia"
        return reporteDet

# Almacena respuesta de alerta de trabajo pendiente
def almacenarRespuesta(respuesta):
    trabajo = Trabajos.objects.get(pk=respuesta['trabajo'])
    segTrabajo = seguimientoTrabajos.objects.get(trabajo=trabajo)
    if segTrabajo.respuestaUser:
        if segTrabajo.respuestaUser == 'Postergar':
            respuesta_bot = "👍 Respuesta registrada - " + str(respuesta['respuesta'])
        else:
            respuesta_bot = "Ya registraste una respuesta el día de hoy para este trabajo."
    else:
        segTrabajo.fechaRespuesta = timezone.now().today()
        segTrabajo.respuestaUser = respuesta['respuesta']
        segTrabajo.save()
        respuesta_bot = "👍 Respuesta registrada - " + str(respuesta['respuesta'])
    return respuesta_bot



# ***   LOGS DE SUCESOS ***

# Registra suceso en donde un cliente se quiere registrar pero su cuit/cuil no está en el sistema.
def clienteNoRegistrado(cuil_cuit, username, nombre):
    logIncidente = registroBotIncidencias()
    logIncidente.fechaSuceso = timezone.now().date()
    logIncidente.observacion = "Cliente con username " + str(username) + " y nombre " + str(nombre) + " ingresó " \
                               "su CUIT/CUIL " + cuil_cuit + " mediante Télegram pero el mismo no está" \
                               " registrado en el sistema."
    logIncidente.save()

# Registra suceso en donde una persona cualquiera, sin usar comandos, quiere interactuar con el bot. (no puede)
# TO-DO, hay que poner una zona horaria a la basura esta
def personaNoRegistrada(username, nombre):
    logIncidente = registroBotIncidencias()
    logIncidente.fechaSuceso = timezone.now().date()
    logIncidente.observacion = "Persona  con username " + str(username) + " y nombre " + str(nombre) + " le mandó " \
                               "un mensaje al bot sin estar registrada como usuario o como cliente."
    logIncidente.save()

