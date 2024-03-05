from os import name
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from .views import cart_views, student_views, course_views, subject_views

app_name = "api_v2"

router = routers.DefaultRouter()

router.register(r'v2/payments', cart_views.PaymentView, basename="view_payments")
router.register(r'v2/orders', cart_views.OrderView, basename="view_orders")
router.register(r'v2/student-certificates', student_views.StudentCertificateView, basename="view_student_certificates")
router.register(r'v2/student-profile', student_views.StudentProfileView, basename="view_student_profile")
router.register(r'v2/enrollments', course_views.EnrollmentView, basename="view_enrollments")
router.register(r'v2/subjects', subject_views.SubjectView, basename="view_subjects")

# router.register(r'course-enrollment',
#                 course_views.EnrollmentViewset, basename ="enrollments"),
# router.register(r'course-assess-rating',
#                 course_views.CourseRatingViewSet),

urlpatterns = [
   

    # path('users/', cart_views.PaymentView.as_view(), name="api_users_list"),
    # path('users/<int:pk>/', cart_views.PaymentView.as_view(), name="api_user_detail"),
   
    path('', include(router.urls)),
]
