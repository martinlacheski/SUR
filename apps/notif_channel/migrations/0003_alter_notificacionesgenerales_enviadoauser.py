# Generated by Django 3.2.6 on 2021-11-13 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notif_channel', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacionesgenerales',
            name='enviadoAUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Usuario al que se le envió la notif'),
        ),
    ]
