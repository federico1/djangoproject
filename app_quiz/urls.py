from django.urls import path, include, re_path
from .views import  question_add, question_delete
from django.views.decorators.cache import cache_page


urlpatterns = [
    path(r'module-quiz/<int:module_id>/',
         question_add, name='app_add_question'),
    path(r'module-quiz-delete/<int:module_id>/',
         question_delete, name='app_delete_question'),
]
