from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from .views import order_view

app_name = "api_backend_v1"

router = routers.DefaultRouter()

router.register(r'v1/orders', order_view.OrderView, basename="view_backend_orders")

urlpatterns = [
    path('', include(router.urls)),
]
