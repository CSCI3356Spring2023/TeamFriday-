# Generated by Django 4.1.7 on 2023-04-02 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="resume",
            field=models.FileField(blank=True, default="", upload_to=""),
        ),
    ]