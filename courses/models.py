from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.conf import settings

from students.models import Quiz


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return f'/course/subject/{self.slug}'

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="courses_joined",
                                      through='Enrollments')

    quiz = models.ForeignKey(Quiz, related_name='quiz',
                             blank=True, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return f'/course/{self.slug}'

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    quiz = models.ForeignKey(Quiz,
                             related_name='module_quiz',
                             blank=True, null=True,
                             on_delete=models.SET_NULL)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={'model__in': ('text',
                                                                     'video',
                                                                     'image',
                                                                     'file',
                                                                     'iframe')},
                                     on_delete=models.CASCADE)
    has_progress = models.BooleanField(default=True)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):

        return render_to_string('courses/content/{}.html'.format(
            self._meta.model_name), {'item': self})


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.TextField()


class IFrame(ItemBase):
    site_url = models.TextField()


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    course = models.ForeignKey(
        Course, related_name='reviews', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    user_name = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reviewers',  on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)


class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def get_members(self):
        return '\n'.join([u.username for u in self.users.all()])


class CourseProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='courses_progress',
                             on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name='content_progress')
    is_completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return str(self.content)


class CourseTimeLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='courses_time_spent',
                             on_delete=models.SET_NULL, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    total_seconds = models.IntegerField(default=0)
    started_time = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course,
                               related_name='time_logs',
                               on_delete=models.CASCADE)

    class Meta:
        db_table = "courses_time_logs"

    def __str__(self):
        return str(self.total_seconds)


class CourseFeature(models.Model):
    course = models.ForeignKey(Course,
                               related_name='features',
                               on_delete=models.CASCADE)
    schedule = models.TextField(blank=True, null=True)
    outcomes = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    completion_requirements = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['pk']
        db_table = "courses_feature"

    def __str__(self):
        return '{}'.format(self.course.id)


class Attendance(models.Model):
    CHECK_IN = 1
    CHECK_OUT = 2

    ATTEND_CHOICES = [
        (CHECK_IN, 'CheckIn'),
        (CHECK_OUT, 'CheckOut'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course,
                               related_name='attendees',
                               on_delete=models.CASCADE)
    event_type = models.IntegerField(choices=ATTEND_CHOICES, default=CHECK_IN)
    is_approved = models.BooleanField(default=False)
    is_bio_verified = models.BooleanField(default=False)
    image = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.event_type)


class Enrollments(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='course_enrolled', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='course_enrolled',
                               on_delete=models.CASCADE)

    is_completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.user)


class StudentCertificate(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='certificates', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='certificates',
                               on_delete=models.CASCADE)
    ref_number = models.CharField(max_length=200)
    file_path = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.event_type)


class Evaluation(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='course_evaluations', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='student_evaluations',
                               on_delete=models.CASCADE)
    recommend = models.TextField(null=False, blank=False)
    class_environment = models.TextField(null=False, blank=False)
    learning_outcomes = models.TextField(null=False, blank=False)
    instructor_knowledge = models.TextField(null=False, blank=False)
    helpful_material = models.TextField(null=False, blank=False)
    learning_opportunities = models.TextField(null=False, blank=False)
    beneficial_class = models.TextField(null=False, blank=False)
    theoretical_experience = models.TextField(null=False, blank=False)
    helpful_growth_career = models.TextField(null=False, blank=False)
    grade_given = models.TextField(null=False, blank=False)
    class_organized = models.TextField(null=False, blank=False)
    instructor_knowledgeable = models.TextField(null=False, blank=False)
    instructor_communication = models.TextField(null=False, blank=False)
    instructor_motivating = models.TextField(null=False, blank=False)
    instructor_methods = models.TextField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.form_id)


class AssessRating(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='course_ratings', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='student_ratings',
                               on_delete=models.CASCADE)
    key_name = models.TextField(null=False, blank=False)
    key_value = models.IntegerField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.key_name)
