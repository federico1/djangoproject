# Generated by Django 2.0.5 on 2021-12-27 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_chat', '0015_externalvideoroom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='owner',
        ),
    ]