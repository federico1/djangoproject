from django import template
from django.core.serializers import serialize
from courses.models import Course

register = template.Library()


@register.filter
def get_enroll(qs, student_user):
    qs = qs.get(user=student_user)
    print(qs)
    return qs
