# Generated by Django 3.2.6 on 2021-10-22 22:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_telegram', '0017_auto_20211022_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrobotincidencias',
            name='fechaRevision',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 22, 19, 17, 13, 161780), null=True),
        ),
        migrations.AlterField(
            model_name='registrobotincidencias',
            name='fechaSuceso',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 22, 19, 17, 13, 161389)),
        ),
        migrations.AlterField(
            model_name='respuestatrabajofinalizado',
            name='fechaRespuesta',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 22, 19, 17, 13, 168486), null=True),
        ),
    ]
