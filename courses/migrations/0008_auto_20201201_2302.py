# Generated by Django 2.0.5 on 2020-12-01 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_coursetimelog'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='coursetimelog',
            table='course_time_logs',
        ),
    ]
