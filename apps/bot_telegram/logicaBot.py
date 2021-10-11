import datetime
from apps.usuarios.models import Usuarios
from apps.erp.models import Clientes
from apps.trabajos.models import *
from apps.bot_telegram.models import *
from apps.parametros.models import EstadoParametros

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

# Chequea que el estado del trabajo esté entre los instanciados en la función cosa de no mostrarle al cliente
# trabajos que ya les fueron entregados o trabajos que se hayan cancelado.
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







