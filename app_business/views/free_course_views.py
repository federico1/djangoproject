from django.views import generic
from django.db.models import Sum
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import json

from app_business.decorators import business_role_required
from app_cart.models import Order, Item, Payment
from app_business.models import BusinessCourses

decorators = [never_cache, login_required, business_role_required]


@method_decorator(decorators, name='dispatch')
class BuyFreeCoursesTemplateView(generic.TemplateView):
    template_name = 'business_free_courses/buy_free.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BuyFreeCoursesTemplateView, self).get_context_data(
            *args, **kwargs)

        free_credits = self.request.user.business_credits.aggregate(
            Sum('credits_remaining'))

        print(free_credits)

        return context
