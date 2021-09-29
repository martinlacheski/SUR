# Generated by Django 3.2.6 on 2021-09-17 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0017_mediospago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiposiva',
            name='iva',
            field=models.FloatField(default=21, verbose_name='Porcentaje'),
        ),
        migrations.AlterField(
            model_name='tipospercepciones',
            name='percepcion',
            field=models.FloatField(default=0, verbose_name='Porcentaje'),
        ),
    ]
