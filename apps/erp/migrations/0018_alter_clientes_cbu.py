# Generated by Django 3.2.6 on 2021-09-08 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0017_auto_20210908_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='cbu',
            field=models.CharField(blank=True, max_length=22, null=True, verbose_name='Clave CBU/CVU'),
        ),
    ]
