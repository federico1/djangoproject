from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class SuperuserRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_superuser


class OrdersView(SuperuserRequiredMixin, generic.TemplateView):
    template_name = 'orders/list.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(OrdersView, self).get_context_data(*args, **kwargs)
        return context


class OrderDetailsView(SuperuserRequiredMixin, generic.TemplateView):
    template_name = 'orders/details.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailsView, self).get_context_data(*args, **kwargs)
        return context