# Generated by Django 3.2.6 on 2021-11-29 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('erp', '0001_initial'),
        ('parametros', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventas',
            name='condicionVenta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='parametros.condicionespago', verbose_name='Condición de pago'),
        ),
        migrations.AddField(
            model_name='ventas',
            name='medioPago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='parametros.mediospago', verbose_name='Medio de pago'),
        ),
    ]
