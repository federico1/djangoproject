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


# for testing the data , dump etc
class TestOpsView(SuperuserRequiredMixin, generic.TemplateView):
    template_name = 'test_ops.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(TestOpsView, self).get_context_data(*args, **kwargs)

        orders = Order.objects.all()

        for order in orders:
            items = order.items.all()
            payments = order.payments.all()

            gateway = None

            if(payments.count()>0):
                gateway = payments.first().gateway
            
            for order_item in items:
                cid = order_item.course_id
                uid = order.user_id

                c_enrollments = Enrollments.objects.filter(course_id=cid, user_id = uid)

                cnt  = c_enrollments.count()


                if cnt == 1:
                    enr = c_enrollments.first()
                    order_item.enrollment = enr
                    order_item.save()

        return context

# class UsersView(generic.TemplateView):
#     template_name = 'admin_users.html'
    
#     def get_context_data(self, *args, **kwargs):
#         context = super(UsersView, self).get_context_data(*args, **kwargs)
#         return context