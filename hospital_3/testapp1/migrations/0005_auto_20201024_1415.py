# Generated by Django 3.0.7 on 2020-10-24 08:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp1', '0004_auto_20201024_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 24, 14, 15, 40, 520573)),
        ),
        migrations.AlterField(
            model_name='registration',
            name='reg_validity',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 24, 14, 15, 40, 520573)),
        ),
    ]
