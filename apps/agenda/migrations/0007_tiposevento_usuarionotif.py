# Generated by Django 3.2.6 on 2021-09-09 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0006_rename_tiemporecordatorio_tiposevento_horariorecordatorio'),
    ]

    operations = [
        migrations.AddField(
            model_name='tiposevento',
            name='usuarioNotif',
            field=models.TextField(default='lwo'),
            preserve_default=False,
        ),
    ]
