# Generated by Django 3.2.6 on 2021-09-06 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0002_alter_tiposiva_iva'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiposiva',
            name='iva',
            field=models.DecimalField(decimal_places=2, default=21, max_digits=9, verbose_name='Porcentaje'),
        ),
    ]
