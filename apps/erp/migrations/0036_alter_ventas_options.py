# Generated by Django 3.2.6 on 2021-09-17 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0035_ventas_estadoventa'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ventas',
            options={'ordering': ['fecha'], 'verbose_name': 'Venta', 'verbose_name_plural': 'Ventas'},
        ),
    ]
