# Generated by Django 4.0.7 on 2023-04-30 00:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_application_related_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='application_status',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='current',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='link',
        ),
        migrations.AddField(
            model_name='notifications',
            name='seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notifications',
            name='timestamp',
            field=models.TimeField(default=datetime.datetime(2023, 4, 29, 20, 20, 26, 829456)),
        ),
    ]