from django.utils import timezone
import datetime
import random
import telegram
from apscheduler.schedulers.background import BlockingScheduler
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from apps.bot_telegram.logicaBot import porcentajeTrabajo, notificarSistema
from apps.bot_telegram.models import seguimientoTrabajos
from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos, DetalleServiciosTrabajo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.db.models import Count
from apps.usuarios.models import Usuarios
from apps.bot_telegram.logicaBot import porcentajeTrabajo

bot = telegram.Bot(token='1974533179:AAFilVMl-Sw4On5h3OTwm4czRULAKMfBWGM')

class Command(BaseCommand):
    def handle(self, *args, **options):
        users_a_evaluar = Usuarios.objects.filter(realizaTrabajos=True)
        if len(users_a_evaluar) < 1:
            return {}
        else:
            # Se obtienen los estados de interés para los trabajos de los usuarios a evaluar
            estados = EstadoParametros.objects.last()
            estados_filter = [estados.estadoEspecial.id, estados.estadoInicial.id, estados.estadoPlanificado.id]

            # Se obtiene un diccionaro que sumariza cuantos trabajos y qué porcentaje de avance tiene cada usuario actualmente
            trab_por_user = []
            for u in users_a_evaluar:
                porcentaje_avance_trabajos = 0
                trabajos_user = Trabajos.objects.filter(usuarioAsignado=u, estadoTrabajo__in=estados_filter)
                for t in trabajos_user:
                    porcentaje_avance_trabajos += float(porcentajeTrabajo(t))
                trab_por_user.append({'usuario': u, 'cant_trab': len(trabajos_user),
                                      'procentaje_avance': porcentaje_avance_trabajos, })

            for t in trab_por_user:
                print(t)
            # Ordenamiento de lista
            trab_por_user.sort(key=orden_cant_trab)

            # Se corrobora si existe un solo user con menor cantidad de trabajos.
            candidato = trab_por_user[0]
            users_candidatos = check_mas_de_uno(candidato, trab_por_user, 'cant_trab')
            if len(users_candidatos) == 1:
                print(str({'id': users_candidatos[0]['usuario'].id, 'text': users_candidatos[0]['usuario'].username}))
            else:
                # Ordenamiento de lista
                trab_por_user.sort(key=orden_avance_trab)

                # Se corrobora si existe un solo user con mayor porcentaje de avance en trabajos.
                candidato = trab_por_user[0]
                users_candidatos = check_mas_de_uno(candidato, trab_por_user, 'procentaje_avance')
                if len(users_candidatos) == 1:
                    print(str({'id': users_candidatos[0]['usuario'].id,
                            'text': users_candidatos[0]['usuario'].username}))
                else:
                    # Random
                    user_final = random.choice(users_candidatos)
                    print(str({'id': user_final['usuario'].id, 'text': user_final['usuario'].username}))

        # Criterior de ordenación por cantidad de trabajos

def orden_cant_trab(dict_user_trabajo):
    return dict_user_trabajo['cant_trab']

    # Criterior de ordenación por porcentaje de avance de trabajos

def orden_avance_trab(dict_user_trabajo):
    return dict_user_trabajo['procentaje_avance']

    # Check si existe más de un user con el concepto que se le indique.  # Returna lista de diccionarios.

def check_mas_de_uno(candidato, trabajos, concepto):
    users_cand = []
    for u in trabajos:
        if u[concepto] == candidato[concepto]:
            users_cand.append(u)
    return users_cand