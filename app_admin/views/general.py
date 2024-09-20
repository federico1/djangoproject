from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from app_cart.models import Order
from courses.models import Enrollments

class SuperuserRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_superuser


class HomeView(SuperuserRequiredMixin, generic.TemplateView):
    template_name = 'admin_home.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        return context
