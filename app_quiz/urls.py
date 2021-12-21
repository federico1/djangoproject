from django.urls import path, include, re_path
from .views import  question_add, question_delete, quiz_course, question_delete_generic, quiz_questions
from django.views.decorators.cache import cache_page


urlpatterns = [
    path(r'module-quiz/<int:module_id>/',
         question_add, name='app_add_question'),
    path(r'module-quiz-delete/<int:module_id>/',
         question_delete, name='app_delete_question'),
    path(r'course-quiz/<int:course_id>/',
         quiz_course, name='quiz_course'),
    path(r'question-delete/<int:question_id>/',
         question_delete_generic, name='question_delete'),
    path(r'quiz-questions/<int:quiz_id>/',
         quiz_questions, name='quiz_question_manager'),
]
