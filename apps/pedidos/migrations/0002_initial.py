# Generated by Django 3.2.6 on 2021-12-01 11:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('erp', '0003_initial'),
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidossolicitud',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='pedidosolicitudproveedor',
            name='pedidoSolicitud',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pedidos.pedidossolicitud', verbose_name='Pedido de Solicitud'),
        ),
        migrations.AddField(
            model_name='pedidosolicitudproveedor',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='erp.proveedores', verbose_name='Proveedor'),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='pedidoSolicitud',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pedidos.pedidossolicitud', verbose_name='Pedido de Solicitud'),
        ),
        migrations.AddField(
            model_name='historicalpedidossolicitud',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalpedidossolicitud',
            name='usuario',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='historicaldetallepedidosolicitud',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaldetallepedidosolicitud',
            name='pedido',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='pedidos.pedidossolicitud'),
        ),
        migrations.AddField(
            model_name='historicaldetallepedidosolicitud',
            name='producto',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='erp.productos', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='detallepedidosolicitudproveedor',
            name='pedidoSolicitudProveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pedidos.pedidosolicitudproveedor'),
        ),
        migrations.AddField(
            model_name='detallepedidosolicitudproveedor',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='erp.productos', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='detallepedidosolicitud',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pedidos.pedidossolicitud'),
        ),
        migrations.AddField(
            model_name='detallepedidosolicitud',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='erp.productos', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pedidos.pedidos'),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='erp.productos', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='erp.proveedores', verbose_name='Proveedor'),
        ),
    ]
