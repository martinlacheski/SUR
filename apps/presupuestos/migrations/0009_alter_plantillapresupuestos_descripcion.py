# Generated by Django 3.2.6 on 2021-10-04 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0008_alter_plantillapresupuestos_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantillapresupuestos',
            name='descripcion',
            field=models.CharField(max_length=100, verbose_name='Descripción'),
        ),
    ]
