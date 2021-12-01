# Generated by Django 3.2.6 on 2021-11-30 22:04

from django.db import migrations, models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalnotifUsuariosBot',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Notificacion de incidencia',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalrespuestaTrabajoFinalizado',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('fechaRespuesta', models.DateTimeField(blank=True, null=True)),
                ('respuesta_puntual', models.DateField(blank=True, null=True)),
                ('respuesta_generica', models.CharField(blank=True, max_length=20, null=True, verbose_name='Respuesta')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Respuesta de trabajo finalizado',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalseguimientoTrabajos',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('cantVecesNotif_dia', models.IntegerField(default=0, verbose_name='Cantidad de veces notificadas en el día')),
                ('cantVecesNotif_total', models.IntegerField(default=0, verbose_name='Cantidad de veces TOTALES notificadas (1 por día)')),
                ('respuestaUser', models.CharField(blank=True, max_length=40, null=True, verbose_name='Respuesta')),
                ('fechaEnvio', models.DateTimeField(blank=True, null=True)),
                ('fechaRespuesta', models.DateTimeField(blank=True, null=True)),
                ('notif_por_sist', models.IntegerField(default=0, verbose_name='Cantidad de veces notificadas por Sistema.')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Seguimiento de estado de trabajo',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='notifUsuariosBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Notificacion de incidencia',
                'verbose_name_plural': 'Notificaciones de incidencia',
                'db_table': 'bot_usuarios_a_notificar',
                'ordering': ['usuario_id'],
            },
        ),
        migrations.CreateModel(
            name='respuestaTrabajoFinalizado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaRespuesta', models.DateTimeField(blank=True, null=True)),
                ('respuesta_puntual', models.DateField(blank=True, null=True)),
                ('respuesta_generica', models.CharField(blank=True, max_length=20, null=True, verbose_name='Respuesta')),
            ],
            options={
                'verbose_name': 'Respuesta de trabajo finalizado',
                'verbose_name_plural': 'Respuestas de trabajo finalizado',
                'db_table': 'bot_respuestaTrabajoFinalziado',
                'ordering': ['fechaRespuesta'],
            },
        ),
        migrations.CreateModel(
            name='seguimientoTrabajos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantVecesNotif_dia', models.IntegerField(default=0, verbose_name='Cantidad de veces notificadas en el día')),
                ('cantVecesNotif_total', models.IntegerField(default=0, verbose_name='Cantidad de veces TOTALES notificadas (1 por día)')),
                ('respuestaUser', models.CharField(blank=True, max_length=40, null=True, verbose_name='Respuesta')),
                ('fechaEnvio', models.DateTimeField(blank=True, null=True)),
                ('fechaRespuesta', models.DateTimeField(blank=True, null=True)),
                ('notif_por_sist', models.IntegerField(default=0, verbose_name='Cantidad de veces notificadas por Sistema.')),
            ],
            options={
                'verbose_name': 'Seguimiento de estado de trabajo',
                'verbose_name_plural': 'Seguimiento de estado de trabajos',
                'db_table': 'bot_seguimientoTrabajos',
                'ordering': ['trabajo'],
            },
        ),
    ]
