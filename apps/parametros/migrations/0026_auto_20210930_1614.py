# Generated by Django 3.2.6 on 2021-09-30 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0025_auto_20210930_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoParametros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estadoEspecial', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='estadoEspecial', to='parametros.estados', verbose_name='Estado Especial')),
                ('estadoInicial', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='estadoInicial', to='parametros.estados', verbose_name='Estado Inicial')),
            ],
            options={
                'verbose_name': 'Estado de Trabajo Parámetros',
                'verbose_name_plural': 'Estado de Trabajos Parámetros',
                'db_table': 'parametros_estado_trabajo_parametros',
            },
        ),
        migrations.DeleteModel(
            name='EstadoEspecial',
        ),
    ]
