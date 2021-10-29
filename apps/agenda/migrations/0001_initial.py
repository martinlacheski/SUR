from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [

        migrations.swappable_dependency(settings.AUTH_USER_MODEL),

    ]

    operations = [
        migrations.CreateModel(
            name='tiposEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('horarioRecordatorio', models.TimeField()),
                ('recordarSistema', models.BooleanField(default=True)),
                ('recordarTelegram', models.BooleanField()),
                ('recordarEmail', models.BooleanField()),
                ('usuarioNotif', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='UsuarioAsoc')),

            ],
            options={
                'verbose_name': 'Tipo de Evento',
                'verbose_name_plural': 'Tipos de Eventos',
                'db_table': 'agenda_tiposEventos',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='eventosAgenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCreacion', models.DateField(default=django.utils.timezone.now)),

                ('fechaNotificacion', models.DateField()),
                ('descripcion', models.TextField()),
                ('repeticion', models.CharField(blank=True, choices=[('DIA', 'Diariamente'), ('SEM', 'Semanalmente'), ('MEN', 'Mensualmente')], max_length=3)),
                ('tipoEvento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='agenda.tiposevento', verbose_name='tipoEvento')),
            ],
            options={
                'verbose_name': 'Evento Agenda',
                'verbose_name_plural': 'Eventos Agenda',
                'db_table': 'agenda_eventosAgenda',
                'ordering': ['fechaCreacion'],
            },
        ),
    ]
