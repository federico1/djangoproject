# Generated by Django 2.0.5 on 2020-05-23 20:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20200519_2230'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_chat', '0004_conversationmember'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('details', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=20)),
                ('participant_count', models.IntegerField(blank=True, default=0, null=True)),
                ('participant_max', models.IntegerField(blank=True, default=2, null=True)),
                ('is_deleted', models.BooleanField(default=0)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_rooms', to='courses.Course')),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['id']},
        ),
    ]