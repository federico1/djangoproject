from django import template
from django.core.serializers import serialize
from courses.models import Course

register = template.Library()


@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None


@register.filter
def jsonify(object):
    json = serialize('json', [object])[1:-1]
    return json
