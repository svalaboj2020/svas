# Generated by Django 3.0.7 on 2020-11-24 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0011_auto_20201124_1704'),
    ]

    operations = [
        migrations.RenameField(
            model_name='out_item_entry',
            old_name='IGST_tax_amount',
            new_name='billed_amount',
        ),
        migrations.RemoveField(
            model_name='out_item_entry',
            name='IGST_tax_per',
        ),
    ]
