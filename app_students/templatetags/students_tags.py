from django import template
from django.core.serializers import serialize
from courses.models import Course

register = template.Library()


@register.filter
def get_enroll(qs, student_user):
    qs = qs.filter(user=student_user).first()
    return qs

@register.filter
def filter_enroll(qs, student_user):
    qs = qs.filter(user=student_user)
    return qs
