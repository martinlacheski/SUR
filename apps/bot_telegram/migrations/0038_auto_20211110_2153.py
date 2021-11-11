# Generated by Django 3.2.6 on 2021-11-11 00:53

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bot_telegram', '0037_auto_20211106_2216'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='notifIncidentesUsuarios',
            new_name='notifUsuariosBot',
        ),
        migrations.RemoveField(
            model_name='registrobotincidencias',
            name='revisadoPor',
        ),
        migrations.AlterField(
            model_name='respuestatrabajofinalizado',
            name='fechaRespuesta',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 10, 21, 53, 33, 786761), null=True),
        ),
        migrations.AlterModelTable(
            name='notifusuariosbot',
            table='bot_usuarios_a_notificar',
        ),
        migrations.DeleteModel(
            name='notificacionUsuarios_Tel',
        ),
        migrations.DeleteModel(
            name='registroBotIncidencias',
        ),
    ]
