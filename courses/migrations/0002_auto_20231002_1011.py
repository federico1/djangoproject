# Generated by Django 2.0.5 on 2023-10-02 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('courses', '0001_initial'),
        ('students', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='text',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studentcertificate',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='courses.Course'),
        ),
        migrations.AddField(
            model_name='studentcertificate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='review',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='courses.Course'),
        ),
        migrations.AddField(
            model_name='review',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='module',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='courses.Course'),
        ),
        migrations.AddField(
            model_name='module',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='module_quiz', to='students.Quiz'),
        ),
        migrations.AddField(
            model_name='image',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='iframe',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iframe_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='file',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_evaluations', to='courses.Course'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_evaluations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enrollments',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_enrolled', to='courses.Course'),
        ),
        migrations.AddField(
            model_name='enrollments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_enrolled', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coursetimelog',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_logs', to='courses.Course'),
        ),
        migrations.AddField(
            model_name='coursetimelog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses_time_spent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courseprogress',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_progress', to='courses.Content'),
        ),
        migrations.AddField(
            model_name='courseprogress',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses_progress', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coursefeature',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='courses.Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='quiz', to='students.Quiz'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='courses_joined', through='courses.Enrollments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='courses.Subject'),
        ),
        migrations.AddField(
            model_name='content',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ('text', 'video', 'image', 'file', 'iframe')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='content',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='courses.Module'),
        ),
        migrations.AddField(
            model_name='cluster',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendance',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendees', to='courses.Course'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assessrating',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_ratings', to='courses.Course'),
        ),
        migrations.AddField(
            model_name='assessrating',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_ratings', to=settings.AUTH_USER_MODEL),
        ),
    ]
