from django.views import generic

class LegalView(generic.TemplateView):
    template_name = "legal/legal.html"


class AboutView(generic.TemplateView):
    template_name = "about/about.html"