# Generated by Django 3.0.7 on 2020-11-24 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0008_auto_20201122_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='out_item_entry',
            name='bill_tax_per',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='out_item_entry',
            name='sell_disc_per',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]