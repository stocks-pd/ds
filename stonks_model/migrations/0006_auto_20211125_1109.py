# Generated by Django 3.2.9 on 2021-11-25 11:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stonks_model', '0005_auto_20211125_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prophetparam',
            name='find_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 25, 11, 9, 3, 282374, tzinfo=utc), verbose_name='Дата подбора параметров'),
        ),
        migrations.AlterField(
            model_name='prophetparam',
            name='stan_backend',
            field=models.CharField(default=None, max_length=200, null=True, verbose_name='Параметр stan_backend'),
        ),
    ]
