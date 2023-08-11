from django.views import generic


class OrdersView(generic.TemplateView):
    template_name = '/orders/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(OrdersView, self).get_context_data(
            *args, **kwargs)
        return context