from django.urls import path
from .views import general, students
# from views.students import StudentsView
# from django.conf import settings

urlpatterns = [
    path('',
         general.HomeView.as_view(),
         name='admin_dashboard'),
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
]
