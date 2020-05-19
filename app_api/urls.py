from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
#router.register('conversations', views.ConversationDetailView)


urlpatterns = [
    #url(r'^', include(router.urls)),
    path('conversations/', views.ConversationDetailView.as_view()),
    path('teacher-courses/', views.TeacherCoursesDetailView.as_view()),
]
