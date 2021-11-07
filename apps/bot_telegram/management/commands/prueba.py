from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.utils import timezone
from apps.usuarios.models import Usuarios, TiposUsuarios

from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos

# Obtención de todos los usuarios que pueden realizar trabajos y cuantos trabajos tiene cada uno.
class Command(BaseCommand):
    def handle(self, *args, **options):
        empsAEvaluar = []
        tiposUser = TiposUsuarios.objects.filter(realizaTrabajos=True)
        users = Usuarios.objects.filter(tipoUsuario__in=tiposUser)
        estados = EstadoParametros.objects.last()
        estados_filter = [estados.estadoEspecial.id, estados.estadoInicial.id, estados.estadoPlanificado.id]
        for u in users:
            t_asig = Trabajos.objects.filter(usuarioAsignado=u, estadoTrabajo__in=estados_filter)
            dict_users = {
                'usuarioAsignado':str(u.id),
                'count':len(t_asig),
            }
            empsAEvaluar.append(dict_users)
        print(empsAEvaluar)
        return empsAEvaluar


