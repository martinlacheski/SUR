# Generated by Django 3.2.6 on 2021-09-04 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0002_alter_tiposiva_iva'),
        ('erp', '0006_alter_subcategorias_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripción')),
                ('abreviatura', models.CharField(max_length=25, verbose_name='Abreviatura')),
                ('codigo', models.CharField(max_length=20, verbose_name='Codigo')),
                ('codigoBarras1', models.CharField(max_length=20, verbose_name='Codigo de Barras 1')),
                ('codigoBarras2', models.CharField(max_length=20, verbose_name='Codigo de Barras 2')),
                ('codigoProveedor', models.CharField(max_length=20, verbose_name='Codigo de Proveedor')),
                ('stockReal', models.IntegerField(default=0, verbose_name='Stock Real')),
                ('stockMinimo', models.IntegerField(default=0, verbose_name='Stock Mínimo')),
                ('reposicion', models.IntegerField(default=0, verbose_name='Pedido Reposición')),
                ('costo', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de Costo')),
                ('utilidad', models.DecimalField(decimal_places=2, default=0.3, max_digits=9, verbose_name='Margen de Utilidad')),
                ('precioVenta', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de Venta')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='product/%Y/%m/%d', verbose_name='Imagen')),
                ('ubicacion', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ubicacion Física')),
                ('observaciones', models.CharField(blank=True, max_length=100, null=True, verbose_name='Observaciones')),
                ('esInsumo', models.BooleanField(default=False)),
                ('iva', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='parametros.tiposiva', verbose_name='Tipo de IVA')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='erp.subcategorias', verbose_name='Subcategoría')),
            ],
        ),
    ]
