from django import template
from django.core.serializers import serialize

register = template.Library()


@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None


@register.filter
def jsonify(object):
    print(type(object))
    return serialize('json', [object])[1:-1]
