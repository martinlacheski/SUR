# Generated by Django 3.2.6 on 2021-12-23 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('erp', '0003_initial'),
        ('trabajos', '0001_initial'),
        ('parametros', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajos',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='trabajos',
            name='usuarioAsignado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='usuarioAsignado', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Asignado'),
        ),
        migrations.AddField(
            model_name='planificacionessemanales',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='historicaltrabajos',
            name='cliente',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='erp.clientes', verbose_name='Cliente'),
        ),
        migrations.AddField(
            model_name='historicaltrabajos',
            name='estadoTrabajo',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='parametros.estados', verbose_name='Estado Trabajo'),
        ),
        migrations.AddField(
            model_name='historicaltrabajos',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaltrabajos',
            name='modelo',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='parametros.modelos', verbose_name='Modelo'),
        ),
        migrations.AddField(
            model_name='historicaltrabajos',
            name='prioridad',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='parametros.prioridades', verbose_name='Prioridad'),
        ),
        migrations.AddField(
            model_name='historicaltrabajos',
            name='usuario',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='historicaltrabajos',
            name='usuarioAsignado',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Asignado'),
        ),
        migrations.AddField(
            model_name='historicalplanificacionessemanales',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalplanificacionessemanales',
            name='usuario',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='historicaldetalleserviciostrabajo',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaldetalleserviciostrabajo',
            name='servicio',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='erp.servicios'),
        ),
        migrations.AddField(
            model_name='historicaldetalleserviciostrabajo',
            name='trabajo',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='trabajos.trabajos'),
        ),
        migrations.AddField(
            model_name='historicaldetalleserviciostrabajo',
            name='usuario',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='historicaldetalleproductostrabajo',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaldetalleproductostrabajo',
            name='producto',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='erp.productos'),
        ),
        migrations.AddField(
            model_name='historicaldetalleproductostrabajo',
            name='trabajo',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='trabajos.trabajos'),
        ),
        migrations.AddField(
            model_name='historicaldetalleproductostrabajo',
            name='usuario',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='historicaldetalleplanificacionessemanales',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaldetalleplanificacionessemanales',
            name='planificacion',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='trabajos.planificacionessemanales'),
        ),
        migrations.AddField(
            model_name='historicaldetalleplanificacionessemanales',
            name='trabajo',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='trabajos.trabajos'),
        ),
        migrations.AddField(
            model_name='detalleserviciostrabajo',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='erp.servicios'),
        ),
        migrations.AddField(
            model_name='detalleserviciostrabajo',
            name='trabajo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='trabajos.trabajos'),
        ),
        migrations.AddField(
            model_name='detalleserviciostrabajo',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='detalleproductostrabajo',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='erp.productos'),
        ),
        migrations.AddField(
            model_name='detalleproductostrabajo',
            name='trabajo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='trabajos.trabajos'),
        ),
        migrations.AddField(
            model_name='detalleproductostrabajo',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='detalleplanificacionessemanales',
            name='planificacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='trabajos.planificacionessemanales'),
        ),
        migrations.AddField(
            model_name='detalleplanificacionessemanales',
            name='trabajo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='trabajos.trabajos'),
        ),
    ]
