# Generated by Django 3.0.7 on 2020-11-03 10:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp1', '0011_auto_20201103_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment_item',
            name='appt_time',
        ),
        migrations.AlterField(
            model_name='registration',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 3, 15, 53, 26, 543009)),
        ),
        migrations.AlterField(
            model_name='registration',
            name='reg_validity',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 3, 15, 53, 26, 543009)),
        ),
    ]
