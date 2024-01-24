from django.views import generic
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from compression_middleware.decorators import compress_page

from .mail_utils import send_contact_alert


@method_decorator(compress_page, name="dispatch")
class PrivacyPolicyView(generic.TemplateView):
    template_name = "privacy/privacy.html"


@method_decorator(compress_page, name="dispatch")
class TermsView(generic.TemplateView):
    template_name = "privacy/terms.html"


@method_decorator(compress_page, name="dispatch")
class RefundView(generic.TemplateView):
    template_name = "privacy/refund.html"


@method_decorator(compress_page, name="dispatch")
class AboutView(generic.TemplateView):
    template_name = "about/about.html"


@method_decorator(compress_page, name="dispatch")
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


@method_decorator(compress_page, name="dispatch")
class StudentManualView(generic.TemplateView):
    template_name = "student_manual/student_manual.html"


@method_decorator(compress_page, name="dispatch")
class FaqView(generic.TemplateView):
    template_name = "faq/faq.html"


@method_decorator(compress_page, name="dispatch")
class PackagesView(generic.TemplateView):
    template_name = "packages/packages.html"


@method_decorator(compress_page, name="dispatch")
def bad_request(request):
    response = redirect('/')
    return response


def post_contact_form(request):
    
    if request.method == 'POST':
        ctx = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'subject': request.POST['subject'],
            'message': request.POST['message'],
        }

        result = send_contact_alert(ctx)

        return JsonResponse({'result': result})   