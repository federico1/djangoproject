from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class SuperuserRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_superuser


class IndexView(SuperuserRequiredMixin, generic.TemplateView):
    template_name = 'packages/index.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        return context