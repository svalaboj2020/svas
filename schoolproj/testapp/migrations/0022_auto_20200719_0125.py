# Generated by Django 3.0.7 on 2020-07-18 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0021_rlink_upload'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rlink_upload',
            old_name='pdf',
            new_name='url',
        ),
    ]