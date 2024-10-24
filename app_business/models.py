from django.db import models
from django.conf import settings
from courses.models import Course

class BusinessEmployee(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='business_students',
                              on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='business_accounts',
                              on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.student.first_name


class BusinessCourses(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='business_course_owner',
                              on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, related_name='buy_business_courses', on_delete=models.CASCADE)
    assign_history = models.TextField(null=True, blank=True)
    is_assigned = models.BooleanField(default=0)
    is_deleted = models.BooleanField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.user_id