from django.views import generic
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from compression_middleware.decorators import compress_page

from django.template.loader import get_template
from django.core.mail import send_mail

from django.views.generic.base import View
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin

@method_decorator(compress_page, name="dispatch")
class CartView(generic.TemplateView):
    template_name = "cart.html"


@method_decorator(compress_page, name="dispatch")
class CheckoutView(LoginRequiredMixin, generic.TemplateView):
    template_name = "checkout.html"


@method_decorator(compress_page, name="dispatch")
class OrderView(generic.TemplateView):
    template_name = "order.html"

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['ref'] = self.kwargs['slug']
        return context


@method_decorator(compress_page, name="dispatch")
class PackageCartView(generic.TemplateView):
    template_name = "package_cart.html"

    def get_context_data(self, **kwargs):
        context = super(PackageCartView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['slug']
        return context


# this is for temporary invoice for some customers, will delete it after
class TempInvoicePaymentView(View):
    template_name = "temp_invoice_payment.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


def SaveTempInvoice(request):

    result = 1

    import json
    from app_cart.models import Order, Payment, Item

    data_json = json.loads(request.body)

    order = Order(status=Order.APPROVED,
                  ref_id=data_json['ref_id'], user_id=2, total_amount=165)
    order.save()

    for item_data in [198, 198, 198, 195, 195, 195]:

        enrollment = None

        Item.objects.create(order=order, enrollment=enrollment,
                            course_id=item_data, price=111, sub_total=111, qty=1)

    Payment.objects.create(order=order, status=Payment.COMPLETED,
                           gateway='gateway', info=data_json['payments'][0]['info'],
                           total_price=data_json['payments'][0]['total_price'],
                           amount_paid=data_json['payments'][0]['amount_paid'])

    send_mail(subject="Payment recv manual", message="Payment made manual", html_message='Payment',
              from_email='mail@pdhsafety.com',
              recipient_list=['shoaib.ijaz8@gmail.com'],
              fail_silently=False)

    return HttpResponse(result)


def SendOrderConfirmMail(request):

    ref = ''
    result = 0

    if 'ref' in request.POST and request.POST['ref'].strip():
        ref = request.POST['ref']

    if ref:
        ctx = {"ref": ref}
        title = "You're in! Here's your order confirmation."

        html_message = get_template(
            "_mail_order_confirm.html").render(ctx)

        send_mail(
            subject=title,
            message=" Thank you for your purchase! This email is to confirm your order with pdhsafety.com",
            html_message=html_message,
            from_email='mail@pdhsafety.com',
            recipient_list=[request.user.email],
            fail_silently=False)
        result = 1

    return HttpResponse(result)


def NotifySystemView(request):

    result = 0

    if request.POST:
        title = request.POST['title']
        body = request.POST['message']

        send_mail(
            subject=title,
            message=body,
            html_message=body,
            from_email='mail@pdhsafety.com',
            recipient_list=['mail@pdhsafety.com'],
            fail_silently=False)

        result = 1

    return HttpResponse(result)