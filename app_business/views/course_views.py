from django.views import generic
from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

import json

from app_cart.models import Order, Item, Payment

from app_business.models import BusinessCourses


@method_decorator([never_cache], name='dispatch')
class BuyCoursesTemplateView(generic.TemplateView):
    template_name = 'business_courses/buy.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BuyCoursesTemplateView, self).get_context_data(
            *args, **kwargs)

        return context


@method_decorator([never_cache], name='dispatch')
class MyCartTemplateView(generic.TemplateView):
    template_name = 'business_courses/cart.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MyCartTemplateView, self).get_context_data(
            *args, **kwargs)

        return context


@method_decorator([never_cache], name='dispatch')
class CheckoutTemplateView(generic.TemplateView):
    template_name = 'business_courses/checkout.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutTemplateView, self).get_context_data(
            *args, **kwargs)

        return context


@method_decorator([never_cache], name='dispatch')
class CheckoutPostOrderView(View):

    def post(self, request, *args, **kwargs):
        try:
            result = False
            json_data = json.loads(request.body)

            order_object = Order.objects.create(
                ref_id=json_data['ref_id'], user=request.user, total_amount=json_data["total_amount"],
                status=Order.APPROVED
            )

            payment_data = json_data["payments"]

            payment_object= Payment.objects.create(order=order_object, status=Payment.COMPLETED, **payment_data)

            for c_item in json_data['items']:
                Item.objects.create(
                    order=order_object, course_id=c_item["course"], price=c_item["price"], sub_total=c_item["sub_total"], qty=c_item["qty"])
                
                for x in range(int(c_item["qty"])):
                    BusinessCourses.objects.create(user=request.user, course_id=c_item["course"])
            
            result = True

            return JsonResponse({'result': result, 'error': False})
        except Exception as ex:
            print(ex)
            return JsonResponse({'result': None, 'error': True, 'ex': ex})


@method_decorator([never_cache], name='dispatch')
class MyCoursesTemplateView(generic.TemplateView):
    template_name = 'business_courses/my_courses.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MyCoursesTemplateView, self).get_context_data(
            *args, **kwargs)

        return context


@method_decorator([never_cache], name='dispatch')
class MyCoursesManageView(View):
    def get(self, request):
        fs = ['id', 'user', 'course', 'course__title', 'course__slug',
        'assign_history', 'is_assigned', 'is_deleted', 'created']
        qs = BusinessCourses.objects.filter(Q(user = request.user)& Q(is_deleted=False)).values(*fs)
        return JsonResponse({"data": list(qs)},safe=False)

    def post(self, request, *args, **kwargs):
        try:

            if 'op_delete' in request.POST and 'id' in request.POST:
                pass
                return JsonResponse({'result': True, 'error': False})

            return JsonResponse({'result': False, 'error': False})
        except Exception as ex:
            return JsonResponse({'result': None, 'error': True, 'ex': ex})

