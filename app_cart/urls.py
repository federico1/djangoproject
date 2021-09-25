from django.urls import path
from .views import CartView, CheckoutView, OrderView

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
]
