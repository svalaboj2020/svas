# Generated by Django 3.0.7 on 2020-11-22 11:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp1', '0019_auto_20201122_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment_item',
            name='status',
            field=models.CharField(choices=[('SCHEDULED', 'SCHEDULED'), ('COMPLETED', 'COMPLETED')], default='SCHEDULED', max_length=15),
        ),
        migrations.AlterField(
            model_name='registration',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 22, 16, 30, 2, 804970)),
        ),
        migrations.AlterField(
            model_name='registration',
            name='reg_validity',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 22, 16, 30, 2, 804970)),
        ),
    ]
