# Generated by Django 4.2.2 on 2023-08-14 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='time_out',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
