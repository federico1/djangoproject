# Generated by Django 2.0.5 on 2021-01-29 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_coursefeature'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='coursefeature',
            table='courses_feature',
        ),
    ]