# Generated by Django 3.2.6 on 2021-11-29 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='chatIdCliente',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='historicalclientes',
            name='chatIdCliente',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
