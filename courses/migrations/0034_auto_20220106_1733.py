# Generated by Django 2.0.5 on 2022-01-06 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0033_auto_20211211_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_enrolled', to=settings.AUTH_USER_MODEL),
        ),
    ]