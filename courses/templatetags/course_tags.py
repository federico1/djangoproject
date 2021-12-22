from django import template
from django.conf import settings
import random

register = template.Library()

@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")