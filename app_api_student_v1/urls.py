from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import profile_views

app_name = "api_student_v1"

router = routers.DefaultRouter()

router.register(r'v1/profile', profile_views.ProfileView, basename="view_student_profile")

urlpatterns = [
    path('', include(router.urls)),
]
