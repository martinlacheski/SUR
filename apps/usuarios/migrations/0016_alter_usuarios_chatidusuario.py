
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0015_merge_20211028_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='chatIdUsuario',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
