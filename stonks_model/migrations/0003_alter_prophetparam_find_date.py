# Generated by Django 3.2.9 on 2021-11-25 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonks_model', '0002_auto_20211125_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prophetparam',
            name='find_date',
            field=models.DateTimeField(null=True, verbose_name='Дата подбора параметров'),
        ),
    ]
