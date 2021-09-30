# Generated by Django 3.2.6 on 2021-09-30 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0032_auto_20210930_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadoparametros',
            name='estadoCancelado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='estadoCancelado', to='parametros.estados', verbose_name='Trabajo Cancelado'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='estadoparametros',
            name='estadoEspecial',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='estadoEspecial', to='parametros.estados', verbose_name='Trabajo Especial'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='estadoparametros',
            name='estadoFinalizado',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.DO_NOTHING, related_name='estadoFinalizado', to='parametros.estados', verbose_name='Trabajo Especial'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='estadoparametros',
            name='estadoInicial',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.DO_NOTHING, related_name='estadoInicial', to='parametros.estados', verbose_name='Trabajo Normal'),
            preserve_default=False,
        ),
    ]
