from django.urls import path
from .views import general, students, packages, subjects, orders
# from views.students import StudentsView
# from django.conf import settings

urlpatterns = [
    path('',
         general.HomeView.as_view(),
         name='admin_dashboard'),
    path('test',
         general.TestOpsView.as_view(),
         name='admin_test'),
#     path('users',
#          views.UsersView.as_view(),
         #name = 'admin_users'),
    path('students',
         students.StudentsView.as_view(),
         name='admin_students'),
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
]
