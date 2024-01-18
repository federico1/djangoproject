from django.views import generic
from django.views.generic.edit import CreateView
from braces.views import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import get_template

from app_students.forms import StudentSignupForm
from app_students.file_utils import uploaded_file
from app_students.mail_utils import send_welcome_mail

from students.models import User
from courses.models import Course


class EditProfileView(generic.TemplateView):
    template_name = 'profile/edit.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EditProfileView, self).get_context_data(
            *args, **kwargs)
        return context