# Generated by Django 3.2.6 on 2021-11-11 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parametros', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geografico', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltipospercepciones',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaltiposiva',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaltiposcomprobantes',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalprioridades',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalmodelos',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalmodelos',
            name='marca',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='parametros.marcas', verbose_name='Marca'),
        ),
        migrations.AddField(
            model_name='historicalmediospago',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalmarcas',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalestados',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalestadoparametros',
            name='estadoCancelado',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='parametros.estados', verbose_name='Trabajo Cancelado'),
        ),
        migrations.AddField(
            model_name='historicalestadoparametros',
            name='estadoEntregado',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='parametros.estados', verbose_name='Trabajo Entregado'),
        ),
        migrations.AddField(
            model_name='historicalestadoparametros',
            name='estadoEspecial',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='parametros.estados', verbose_name='Trabajo Especial'),
        ),
        migrations.AddField(
            model_name='historicalestadoparametros',
            name='estadoFinalizado',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='parametros.estados', verbose_name='Trabajo Finalizado'),
        ),
        migrations.AddField(
            model_name='historicalestadoparametros',
            name='estadoInicial',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='parametros.estados', verbose_name='Trabajo Normal'),
        ),
        migrations.AddField(
            model_name='historicalestadoparametros',
            name='estadoPlanificado',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='parametros.estados', verbose_name='Trabajo Planificado'),
        ),
        migrations.AddField(
            model_name='historicalestadoparametros',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalempresa',
            name='condicionIVA',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='parametros.condicionesiva', verbose_name='Condición frente al IVA'),
        ),
        migrations.AddField(
            model_name='historicalempresa',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalempresa',
            name='localidad',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='geografico.localidades', verbose_name='Localidad'),
        ),
        migrations.AddField(
            model_name='historicalcondicionespago',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcondicionesiva',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='estadoparametros',
            name='estadoCancelado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='estadoCancelado', to='parametros.estados', verbose_name='Trabajo Cancelado'),
        ),
        migrations.AddField(
            model_name='estadoparametros',
            name='estadoEntregado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='estadoEntregado', to='parametros.estados', verbose_name='Trabajo Entregado'),
        ),
        migrations.AddField(
            model_name='estadoparametros',
            name='estadoEspecial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='estadoEspecial', to='parametros.estados', verbose_name='Trabajo Especial'),
        ),
        migrations.AddField(
            model_name='estadoparametros',
            name='estadoFinalizado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='estadoFinalizado', to='parametros.estados', verbose_name='Trabajo Finalizado'),
        ),
        migrations.AddField(
            model_name='estadoparametros',
            name='estadoInicial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='estadoInicial', to='parametros.estados', verbose_name='Trabajo Normal'),
        ),
        migrations.AddField(
            model_name='estadoparametros',
            name='estadoPlanificado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='estadoPlanificado', to='parametros.estados', verbose_name='Trabajo Planificado'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='condicionIVA',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='parametros.condicionesiva', verbose_name='Condición frente al IVA'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='geografico.localidades', verbose_name='Localidad'),
        ),
        migrations.AlterUniqueTogether(
            name='modelos',
            unique_together={('marca', 'nombre')},
        ),
    ]
