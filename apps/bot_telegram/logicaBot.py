from apps.usuarios.models import Usuarios
from apps.erp.models import Clientes

def check_chatid_cliente(chat_id):
    clientes = Clientes.objects.all()
    for cliente in clientes:
        if cliente.chatIdCliente == int(chat_id):
            return True
    return False

def check_chatid_user(chat_id):
    usuarios = Usuarios.objects.all()
    for user in usuarios:
        if user.chatIdUsuario == int(chat_id):
            return True
    return False