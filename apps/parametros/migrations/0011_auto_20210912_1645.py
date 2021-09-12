# Generated by Django 3.2.6 on 2021-09-12 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0010_auto_20210912_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelos',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterUniqueTogether(
            name='modelos',
            unique_together={('marca', 'nombre')},
        ),
    ]
