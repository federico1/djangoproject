from django.urls import path
from .views import CartView, CheckoutView, OrderView, PackageCartView

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
]
