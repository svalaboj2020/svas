# Generated by Django 3.0.7 on 2020-11-22 10:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp1', '0015_auto_20201120_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 22, 15, 36, 7, 155245)),
        ),
        migrations.AlterField(
            model_name='registration',
            name='reg_validity',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 22, 15, 36, 7, 155245)),
        ),
    ]
