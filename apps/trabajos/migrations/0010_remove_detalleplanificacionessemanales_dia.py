# Generated by Django 3.2.6 on 2021-10-08 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trabajos', '0009_auto_20211008_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalleplanificacionessemanales',
            name='dia',
        ),
    ]
