from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from . import views
from .more_views import course_views, users_views, chat_views, attendance_views

router = routers.DefaultRouter()
#router.register('conversations', views.ConversationDetailView)

router.register(r'courses', course_views.CourseViewset, basename="course")
router.register(r'course-enrollment', course_views.EnrollmentViewset, "enrollment"),
#router.register(r'^course-enrollment/{pk}/update-completed', course_views.EnrollmentViewset.set_completed, "enrollment"),

urlpatterns = [
    #url(r'^', include(router.urls)),
    path('conversations/', views.ConversationDetailView.as_view()),
    path('conversations/<int:pk>/', views.ConversationDetailView.as_view()),
    path('teacher-courses/', views.TeacherCoursesDetailView.as_view()),
    path('teacher-students/', views.TeacherStudentsList.as_view()),
    path('conversation-members/', views.ConversationMembersList.as_view()),
    path('conversation-members/<int:pk>/',
         views.ConversationMembersList.as_view()),
    path('messages/', views.MessageList.as_view()),

    path('video-rooms/', views.VideoRoomDetailView.as_view()),
    path('video-rooms/<int:pk>/', views.VideoRoomDetailView.as_view()),

    path('video-participants/', views.VideoParticipantView.as_view()),
    path('video-participants/<int:pk>/', views.VideoParticipantView.as_view()),

    path('notifications/', views.NotificationDetailView.as_view()),

    path('video-participantslog/', views.ParticipantLogDetailView.as_view()),
    path('video-participantslog/<int:pk>/',
         views.ParticipantLogDetailView.as_view()),

    path('video-courses/', views.VideoCoursesView.as_view()),
    path('video-courses/<int:pk>/', views.VideoCoursesView.as_view()),

    path('subjects/', course_views.SubjectDetailView.as_view()),
    path('subjects/<int:pk>/', course_views.SubjectDetailView.as_view()),

    path('courses_time_logs/', course_views.CourseTimeLogDetailView.as_view()),

    path('add-content-progress/', course_views.AddContentProgressApiView.as_view()),
    
    path('users/', users_views.UserDetailView.as_view()),
    path('users/<int:pk>/', users_views.UserDetailView.as_view()),

 #   path('course-enrollment/', course_views.EnrollmentViewset),
    
    path('sst-cards/', users_views.SSTCardApiView.as_view()),
    
    path('enable-content-progress/', course_views.UpdateHasProgress),

    path('course-features/', course_views.CourseFeatureApiView.as_view()),
    path('course-features/<int:pk>/', course_views.CourseFeatureApiView.as_view()),

    path('external-video-room/', chat_views.ExternalVideoRoomDetailView.as_view()),
    path('external-video-room/<int:pk>/', chat_views.ExternalVideoRoomDetailView.as_view()),

    path('attendance/', attendance_views.AttendanceApiView.as_view()),
    path('attendance/<int:pk>/', attendance_views.AttendanceApiView.as_view()),
    path('approve-attendance/', attendance_views.ApproveAttendance),
    
    path('course-evaluation/', course_views.CourseEvaluationApiView.as_view()),
    path('course-assess-rating/', course_views.CourseRatingApiView.as_view()),

    path('save-base64/', views.SaveBase64ImageView),

    path('', include(router.urls)),
]