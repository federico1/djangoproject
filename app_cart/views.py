from django.views import generic
from django.utils.decorators import method_decorator
from compression_middleware.decorators import compress_page


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

