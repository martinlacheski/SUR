# Generated by Django 3.2.6 on 2021-08-24 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_alter_usuarios_telefono'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarios',
            name='tipoUsuario',
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='usuarios/%Y/%m/%d', verbose_name='Imagen'),
        ),
    ]
