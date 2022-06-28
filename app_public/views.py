from django.views import generic
from django.http import JsonResponse

from .mail_utils import send_contact_alert

class LegalView(generic.TemplateView):
    template_name = "legal/legal.html"


class AboutView(generic.TemplateView):
    template_name = "about/about.html"


class ContactView(generic.TemplateView):
    template_name = "contact/contact.html"

    def post(self, request, *args, **kwargs):

        ctx = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'subject': request.POST['subject'],
            'message': request.POST['message'],
        }

        result = send_contact_alert(ctx)

        return JsonResponse({'result': result})


class StudentManualView(generic.TemplateView):
    template_name = "student_manual/student_manual.html"


class FaqView(generic.TemplateView):
    template_name = "faq/faq.html"


class PackagesView(generic.TemplateView):
    template_name = "packages/packages.html"
