from django.urls import path
from .views import CartView, CheckoutView, OrderView, PackageCartView, SendOrderConfirmMail, TempInvoicePaymentView, SaveTempInvoice

urlpatterns = [
    path('cart/',
         CartView.as_view(),
         name='cart_detail'),
    path('checkout/',
         CheckoutView.as_view(),
         name='checkout_detail'),
    path('order/<slug:slug>/',
         OrderView.as_view(),
         name='order_detail'),
    path('package-buy/<slug:slug>/',
         PackageCartView.as_view(),
         name='package_cart'),
    
    path('invoice-manual/',
         TempInvoicePaymentView.as_view(),
         name='temp_invoice_manaul'),
    path('save-invoice-manual',
         SaveTempInvoice,
         name='save_temp_invoice_manaul'),

    path('send-order-confirm-mail',
         SendOrderConfirmMail,
         name='send_order_confirm_mail'),
]
