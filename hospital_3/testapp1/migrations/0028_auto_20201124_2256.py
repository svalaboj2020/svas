# Generated by Django 3.0.7 on 2020-11-24 17:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp1', '0027_auto_20201124_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 24, 22, 56, 56, 82470)),
        ),
        migrations.AlterField(
            model_name='registration',
            name='reg_validity',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 24, 22, 56, 56, 82470)),
        ),
    ]
