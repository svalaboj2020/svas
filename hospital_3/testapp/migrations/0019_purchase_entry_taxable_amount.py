# Generated by Django 3.0.7 on 2020-11-26 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0018_auto_20201126_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_entry',
            name='taxable_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=19),
        ),
    ]