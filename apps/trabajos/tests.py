import datetime

from django.test import TestCase
from apps.bot_telegram.models import respuestaTrabajoFinalizado
from apps.erp.models import Clientes
from apps.trabajos.models import Trabajos

class CategoriaTestCase(TestCase):

    def test_resp_trab(self):
        Cliente = Clientes.objects.get(pk=1)
        Trabajo = Trabajos.objects.last()
        respuestaTrabajoFinalizado.objects.create(
            cliente=Cliente,
            trabajo=Trabajo,
            fechaRespuesta=datetime.datetime.now(),
            respuesta_puntual=datetime.date.today(),
            respuesta_generica="alo",
        )
        resp = respuestaTrabajoFinalizado.objects.get(respuesta_generica="alo")
        self.assertEqual(resp.respuesta_puntual, datetime.date.today())