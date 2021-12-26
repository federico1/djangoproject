from django.urls import path
from django.views.decorators.cache import cache_page
from .views import main_views, profile_views, quiz_views

urlpatterns = [
     path('register/', main_views.StudentRegistrationView.as_view(),
         name='student_registration'),
     path('uploadfile', main_views.file_upload, name='upload-file'),
     path('', main_views.StudentHomeView.as_view(),
         name='student_dashboard'),
     path('courses', main_views.CourseListView.as_view(),
         name='student_courses'),
    path('course/<int:pk>/', cache_page(60 * 15)
         (main_views.CourseDetailView.as_view()), name='student_course_detail'),
    path('course/<int:pk>/<int:module_id>/', cache_page(60 * 15)
         (main_views.CourseDetailView.as_view()), name='student_course_detail_module'),
    
    path('quiz/<int:pk>/', quiz_views.take_quiz, name='student_take_quiz'),
    path('quiz-reset/<int:pk>/', quiz_views.quiz_reset, name='student_reset_quiz'),
    path('quiz-taken/', quiz_views.TakenQuizTemplateView.as_view(), name='student_taken_quiz'),

     path('edit-profile', profile_views.EditProfileView.as_view(),
         name='student_edit_profile'),
]
