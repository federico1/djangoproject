# Generated by Django 2.0.5 on 2021-12-15 09:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0011_auto_20210521_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]