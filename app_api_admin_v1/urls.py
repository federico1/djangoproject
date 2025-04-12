from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from .views import order_views, cart_views, course_rating_views

app_name = "api_admin_v1"

router = routers.DefaultRouter()

router.register(r'v1/orders', order_views.OrderView,
                basename="view_admin_orders")
router.register(r'v1/packages', cart_views.PackageView,
                basename="view_admin_packages")
router.register(r'v1/assess-ratings', course_rating_views.AssessRatingView,
                basename="view_admin_asess_ratings")
urlpatterns = [
    path('', include(router.urls)),
]
