# Generated by Django 3.0.7 on 2020-07-17 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0018_assignment_upload_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='classx',
            field=models.CharField(default=1, max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='lname',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]