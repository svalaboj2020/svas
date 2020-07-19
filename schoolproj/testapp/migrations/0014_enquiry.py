# Generated by Django 3.0.7 on 2020-07-09 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0013_auto_20200709_0129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('phone', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('message', models.CharField(max_length=255)),
            ],
        ),
    ]