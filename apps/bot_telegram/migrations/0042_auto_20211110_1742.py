# Generated by Django 3.2.6 on 2021-11-10 20:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_telegram', '0041_auto_20211110_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalregistrobotincidencias',
            name='fechaRevision',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 10, 17, 42, 22, 540272), null=True),
        ),
        migrations.AlterField(
            model_name='historicalregistrobotincidencias',
            name='fechaSuceso',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 10, 17, 42, 22, 540217)),
        ),
        migrations.AlterField(
            model_name='historicalrespuestatrabajofinalizado',
            name='fechaRespuesta',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 10, 17, 42, 22, 543368), null=True),
        ),
        migrations.AlterField(
            model_name='registrobotincidencias',
            name='fechaRevision',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 10, 17, 42, 22, 540272), null=True),
        ),
        migrations.AlterField(
            model_name='registrobotincidencias',
            name='fechaSuceso',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 10, 17, 42, 22, 540217)),
        ),
        migrations.AlterField(
            model_name='respuestatrabajofinalizado',
            name='fechaRespuesta',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 10, 17, 42, 22, 543368), null=True),
        ),
    ]
