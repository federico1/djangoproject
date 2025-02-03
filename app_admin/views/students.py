from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import logout, authenticate, login
from students.models import User


class SuperuserRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_superuser


class StudentsView(SuperuserRequiredMixin, generic.TemplateView):
    template_name = 'students/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentsView, self).get_context_data(*args, **kwargs)
        return context


class EvaluationListView(SuperuserRequiredMixin, generic.TemplateView):
    template_name = 'students/evaluation_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EvaluationListView, self).get_context_data(
            *args, **kwargs)
        return context


class AssessmentView(SuperuserRequiredMixin, generic.TemplateView):
    template_name = 'students/assessment.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AssessmentView, self).get_context_data(*args, **kwargs)
        return context


class ImpersonateUserView(SuperuserRequiredMixin, generic.View):
    def get(self, request, pk):
        logout(self.request)
        user = User.objects.get(pk=pk)
        login(self.request, user)
        return HttpResponseRedirect("/")


class SwitchUserToStudentView(SuperuserRequiredMixin, generic.View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        user.is_student = True
        user.is_business = False
        user.save()
        return HttpResponseRedirect("/")
