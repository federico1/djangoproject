from django.views import generic
from django.utils.decorators import method_decorator
from compression_middleware.decorators import compress_page


@method_decorator(compress_page, name="dispatch")
class IACETAccreditation(generic.TemplateView):
    template_name = "blog/iacet.html"
