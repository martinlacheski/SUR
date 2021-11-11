# Generated by Django 3.2.6 on 2021-11-10 14:33

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('geografico', '0005_historicallocalidades_historicalpaises_historicalprovincias'),
        ('usuarios', '0017_auto_20211110_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalUsuarios',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('legajo', models.CharField(blank=True, db_index=True, max_length=10, null=True, verbose_name='Legajo')),
                ('fechaIngreso', models.DateField(blank=True, null=True, verbose_name='Fecha de Ingreso')),
                ('cuil', models.CharField(blank=True, db_index=True, max_length=11, null=True, verbose_name='Cuil')),
                ('direccion', models.CharField(blank=True, max_length=100, null=True, verbose_name='Dirección')),
                ('telefono', models.CharField(blank=True, max_length=100, null=True, verbose_name='Teléfono')),
                ('imagen', models.TextField(blank=True, max_length=100, null=True, verbose_name='Imagen')),
                ('chatIdUsuario', models.IntegerField(blank=True, default=None, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('localidad', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='geografico.localidades', verbose_name='Localidad')),
            ],
            options={
                'verbose_name': 'historical Usuario',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
