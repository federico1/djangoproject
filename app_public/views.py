from django.views import generic

class LegalView(generic.TemplateView):
    template_name = "legal/legal.html"


class AboutView(generic.TemplateView):
    template_name = "about/about.html"


class ContactView(generic.TemplateView):
    template_name = "contact/contact.html"


class StudentManualView(generic.TemplateView):
    template_name = "student_manual/student_manual.html"


class FaqView(generic.TemplateView):
    template_name = "faq/faq.html"


class PackagesView(generic.TemplateView):
    template_name = "packages/packages.html"