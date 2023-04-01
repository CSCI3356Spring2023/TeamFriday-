# Generated by Django 4.0.7 on 2023-03-31 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='instructor',
            new_name='professor',
        ),
        migrations.AddField(
            model_name='instructor',
            name='course_list',
            field=models.ManyToManyField(blank=True, default='', to='main.course'),
        ),
        migrations.AddField(
            model_name='student',
            name='applications',
            field=models.ManyToManyField(blank=True, default='', to='main.application'),
        ),
    ]