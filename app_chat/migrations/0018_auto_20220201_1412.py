# Generated by Django 2.0.5 on 2022-02-01 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_chat', '0017_auto_20220106_1733'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['id']},
        ),
    ]