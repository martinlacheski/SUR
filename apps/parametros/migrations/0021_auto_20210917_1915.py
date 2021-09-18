# Generated by Django 3.2.6 on 2021-09-17 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0020_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='empresas/%Y/%m/%d', verbose_name='Imagen'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='facebook',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Cuenta de Facebook'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='instagram',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Cuenta de Instagram'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='paginaWeb',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Dirección de Página Web'),
        ),
    ]
