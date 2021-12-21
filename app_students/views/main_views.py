from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import get_template

from app_students.forms import StudentSignupForm
from app_students.file_utils import uploaded_file
from app_students.mail_utils import send_welcome_mail

from students.models import User


class StudentRegistrationView(CreateView):
    model = User
    template_name = 'registration/signup_form.html'
    form_class = StudentSignupForm

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        print(self.request.GET.get('next'))
        return super().get_context_data(**kwargs)

    def form_valid(self, form):

        result = super(StudentRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['email'], password=cd['password1'])
        login(self.request, user)
        
        send_welcome_mail(cd)

        return result

    def get_success_url(self):

        if self.request.GET.get('next'):
            return self.request.GET.get('next') + "#register=success"
        
        return reverse_lazy('cart_detail') + '?register=success'


def file_upload(request):

    result = 0

    if request.method == 'POST' and request.FILES['file']:
        result = uploaded_file(request.FILES['file'])

    return HttpResponse(result)
