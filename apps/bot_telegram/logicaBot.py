import datetime
from apps.usuarios.models import Usuarios
from apps.erp.models import Clientes
from django.core.exceptions import *
from apps.trabajos.models import *
from apps.bot_telegram.models import *
from apps.parametros.models import EstadoParametros
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

# Calcula porcentaje de realización de un trabajo
def porcentajeTrabajo(trabajo):
    cantTrabajos = 0
    cantTrabajosRealizados = 0
    detalle = DetalleServiciosTrabajo.objects.filter(trabajo_id=trabajo.id)
    for d in detalle:
        cantTrabajos += 1
        if d.estado:
            cantTrabajosRealizados += 1
    porcentaje = cantTrabajosRealizados / cantTrabajos
    return str(porcentaje * 100)

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

# Registra la respuesta del cliente respecto a cuándo va a buscar el trabajo finalizado.
def registrarRetiro(respuesta):
    resp_to_dict = ast.literal_eval(respuesta)
    log_respuesta = respuestaTrabajoFinalizado()
    try:  # Estará el trabajo y el cliente aún registrado?
        log_respuesta.trabajo = Trabajos.objects.get(pk=int(resp_to_dict['trabajo']))
        log_respuesta.cliente = Clientes.objects.get(pk=int(resp_to_dict['cliente']))
    except ObjectDoesNotExist:
        respuesta = "❌ Ha ocurrido un problema. Probablemnte tu trabajo o vos fueron dados de baja del sistema."
        return {'proc': False, 'respuesta' : respuesta}
    log_respuesta.fechaRespuesta = datetime.datetime.today()
    respuesta = "Hola! 😌\nTe informo que el cliente " + str(log_respuesta.cliente) +\
                ", en respuesta a su trabajo finalizado Nro° " + str(resp_to_dict['trabajo']) + ", informó que lo" \
                " pasará a buscar el día ("
    if 'hoy' in resp_to_dict:
        log_respuesta.respuesta_puntual = datetime.datetime.strptime(resp_to_dict['hoy'], '%Y-%m-%d').date()
        log_respuesta.respuesta_generica = "El cliente pasará a buscar el trabajo finalizado el día de hoy (" +\
                                            str(datetime.datetime.strptime(resp_to_dict['hoy'],
                                                                           '%Y-%m-%d').date().strftime('%d-%m-%Y')) +\
                                            ")."
        respuesta += str(datetime.datetime.strptime(resp_to_dict['hoy'], '%Y-%m-%d').date().strftime('%d-%m-%Y')) + ")"
    elif 'sig_dia_habil' in resp_to_dict:
        log_respuesta.respuesta_puntual = datetime.datetime.strptime(resp_to_dict['sig_dia_habil'], '%Y-%m-%d').date()
        log_respuesta.respuesta_generica = "El cliente pasará a buscar el trabajo finalizado el día " + \
                                           str(datetime.datetime.strptime(resp_to_dict['sig_dia_habil'],
                                                                          '%Y-%m-%d').date().strftime('%d-%m-%Y')) + \
                                           ")."
        respuesta += str(datetime.datetime.strptime(resp_to_dict['sig_dia_habil'], '%Y-%m-%d').date().strftime('%d-%m-%Y')) + ")"
    elif 'se_secomunica' in resp_to_dict:
        log_respuesta.respuesta_generica = "El cliente se comunicará personalmente."
        respuesta = "Hola! 😌\nTe informo que el cliente " + str(log_respuesta.cliente) + \
                    ", en respuesta a su trabajo finalizado Nro° " + str(resp_to_dict['trabajo']) + ", " \
                    "informó que se comunicará personalmente para retirar dicho trabajo"
    log_respuesta.save()
    return {'proc': True, 'respuesta': respuesta}


# ***   USUARIOS ***

#   Chequea si el usuario ya registrado se quiere registrar como cliente. (no va a poder)
def check_chatid_cliente(chat_id):
    clientes = Clientes.objects.all()
    for cliente in clientes:
        if cliente.chatIdCliente == int(chat_id):
            return True
    return False



# ***   LOGS DE SUCESOS ***

# Registra suceso en donde un cliente se quiere registrar pero su cuit/cuil no está en el sistema.
def clienteNoRegistrado(cuil_cuit, username, nombre):
    logIncidente = registroBotIncidencias()
    logIncidente.fechaSuceso = datetime.datetime.today()
    logIncidente.observacion = "Cliente con username " + str(username) + " y nombre " + str(nombre) + " ingresó " \
                               "su CUIT/CUIL " + cuil_cuit + " mediante Télegram pero el mismo no está" \
                               " registrado en el sistema."
    logIncidente.save()

# Registra suceso en donde una persona cualquiera, sin usar comandos, quiere interactuar con el bot. (no puede)
# TO-DO, hay que poner una zona horaria a la basura esta
def personaNoRegistrada(username, nombre):
    logIncidente = registroBotIncidencias()
    logIncidente.fechaSuceso = datetime.datetime.today()
    logIncidente.observacion = "Persona  con username " + str(username) + " y nombre " + str(nombre) + " le mandó " \
                               "un mensaje al bot sin estar registrada como usuario o como cliente."
    logIncidente.save()


# *** PROCESOS GENERALES ***



