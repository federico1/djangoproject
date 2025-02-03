from django.urls import path
from .views import general, students, packages, subjects, orders
# from views.students import StudentsView
# from django.conf import settings

urlpatterns = [
    path('',
         general.HomeView.as_view(),
         name='admin_dashboard'),
    path('students',
         students.StudentsView.as_view(),
         name='admin_students'),
    path('ImpersonateUser/<int:pk>/',
         students.ImpersonateUserView.as_view(),
         name='impersonate_user'),
    path('SwitchToStudent/<int:pk>/',
         students.SwitchUserToStudentView.as_view(),
         name='admin_switch_to_student'),
    path('evaluations',
         students.EvaluationListView.as_view(),
         name='admin_evaluations'),
    path('assessments',
         students.AssessmentView.as_view(),
         name='admin_assessments'),
    path('packages',
         packages.IndexView.as_view(),
         name='admin_packages'),
    path('subjects',
         subjects.IndexView.as_view(),
         name='admin_subjects'),
    path('orders',
         orders.OrdersView.as_view(),
         name='admin_orders'),
    path('orders/<int:pk>/', orders.OrderDetailsView.as_view(),
         name='admin_order_details'),
]
