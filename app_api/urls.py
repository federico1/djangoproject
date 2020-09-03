from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from . import views
from .more_views import course_views, users_views

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

    path('notifications/', views.NotificationDetailView.as_view()),

    path('video-participantslog/', views.ParticipantLogDetailView.as_view()),
    path('video-participantslog/<int:pk>/', views.ParticipantLogDetailView.as_view()),

    path('video-courses/', views.VideoCoursesView.as_view()),
    path('video-courses/<int:pk>/', views.VideoCoursesView.as_view()),

    path('subjects/', course_views.SubjectDetailView.as_view()),
    path('subjects/<int:pk>/', course_views.SubjectDetailView.as_view()),

    path('courses/', course_views.CourseDetailView.as_view()),
    path('courses/<int:pk>/', course_views.CourseDetailView.as_view()),

    path('users/', users_views.UserDetailView.as_view()),
    path('users/<int:pk>/', users_views.UserDetailView.as_view()),

]
