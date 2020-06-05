from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
#router.register('conversations', views.ConversationDetailView)


urlpatterns = [
    #url(r'^', include(router.urls)),
    path('conversations/', views.ConversationDetailView.as_view()),
    path('conversations/<int:pk>/', views.ConversationDetailView.as_view()),
    path('teacher-courses/', views.TeacherCoursesDetailView.as_view()),
    path('teacher-students/', views.TeacherStudentsList.as_view()),
    path('conversation-members/', views.ConversationMembersList.as_view()),
    path('conversation-members/<int:pk>/', views.ConversationMembersList.as_view()),
    path('messages/', views.MessageList.as_view()),

    path('video-rooms/', views.VideoRoomDetailView.as_view()),
    path('video-rooms/<int:pk>/', views.VideoRoomDetailView.as_view()),

    path('video-participants/', views.VideoParticipantView.as_view()),
    path('video-participants/<int:pk>/', views.VideoParticipantView.as_view()),

]
