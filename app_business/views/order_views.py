from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import Http404
from braces.views import LoginRequiredMixin

from app_cart.models import Order


class PurchaseHistoryView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'business_orders/purchase_history.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PurchaseHistoryView, self).get_context_data(
            *args, **kwargs)
        return context


class InvoiceView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'business_orders/invoice.html'

    def get_context_data(self, *args, **kwargs):
        context = super(InvoiceView, self).get_context_data(
            *args, **kwargs)

        ref_id = kwargs['ref']
        item_id = kwargs['item']

        if ref_id is not None and item_id is not None:
            order = get_object_or_404(Order, ref_id=ref_id)
            
            if order.user_id != self.request.user.id:
                raise Http404

            context['order'] = order
            context['item_id'] = item_id

        return context


class ReceiptView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'business_orders/receipt.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ReceiptView, self).get_context_data(
            *args, **kwargs)

        ref_id = kwargs['ref']
        item_id = kwargs['item']

        if ref_id is not None and item_id is not None:
            order = get_object_or_404(Order, ref_id=ref_id)
            
            if order.user_id != self.request.user.id:
                raise Http404

            context['order'] = order
            context['item_id'] = item_id

        return context
