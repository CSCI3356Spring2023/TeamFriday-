# Generated by Django 4.0.7 on 2023-04-30 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_notifications_application_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='timestamp',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
