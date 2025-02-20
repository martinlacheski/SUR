# Generated by Django 3.2.6 on 2021-12-23 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notif_channel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacionesgenerales',
            name='enviadoAUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Usuario al que se le envió la notif'),
        ),
        migrations.AddField(
            model_name='historicalnotificacionesgenerales',
            name='enviadoAUser',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario al que se le envió la notif'),
        ),
        migrations.AddField(
            model_name='historicalnotificacionesgenerales',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
