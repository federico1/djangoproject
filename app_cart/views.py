from django.views import generic


class CartView(generic.TemplateView):
    template_name = "cart.html"


class CheckoutView(generic.TemplateView):
    template_name = "checkout.html"


class OrderView(generic.TemplateView):
    template_name = "order.html"

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['ref'] = self.kwargs['slug']
        return context
