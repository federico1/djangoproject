from django.views import generic

class SSTVerifyView(generic.TemplateView):
    template_name = "sst/verify.html"