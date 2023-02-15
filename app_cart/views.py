from django.views import generic
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from compression_middleware.decorators import compress_page

from django.template.loader import get_template
from django.core.mail import send_mail

@method_decorator(compress_page, name="dispatch")
class CartView(generic.TemplateView):
    template_name = "cart.html"


@method_decorator(compress_page, name="dispatch")
class CheckoutView(generic.TemplateView):
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


def SendOrderConfirmMail(request):
  
    ref = ''
    result = 0

    if 'ref' in request.POST and request.POST['ref'].strip():
        ref = request.POST['ref']

    if ref:
        ctx = {ref:ref}
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