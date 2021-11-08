from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.utils import timezone
from apps.usuarios.models import Usuarios, TiposUsuarios

from apps.parametros.models import EstadoParametros
from apps.trabajos.models import Trabajos
from django.contrib.auth.models import Group
from django.forms import model_to_dict

# Obtención de todos los usuarios que pueden realizar trabajos y cuantos trabajos tiene cada uno.
class Command(BaseCommand):
    def handle(self, *args, **options):
        grupos = Group.objects.all().defer('permissions')
        for g in grupos:
            g = model_to_dict(g)
            del g['permissions']
            print(g)



