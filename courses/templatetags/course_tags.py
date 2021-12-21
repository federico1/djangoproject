from django import template
import random

register = template.Library()


# @register.filter
# def model_name(obj):
#     try:
#         return obj._meta.model_name
#     except AttributeError:
#         return None

@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)