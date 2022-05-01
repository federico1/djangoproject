from os import name
from django.conf.urls import url, include
from django.urls import path

from rest_framework import routers

from .more_views import course_views, users_views, chat_views, attendance_views, \
    student_views, cart_views, quiz_views, tag_views, course_module_views

from . import views

router = routers.DefaultRouter()

router.register(r'courses', course_views.CourseViewset, basename="course")
router.register(r'course-enrollment',
                course_views.EnrollmentViewset, "enrollment"),
router.register(r'course-assess-rating',
                course_views.CourseRatingViewSet),

urlpatterns = [
    #url(r'^', include(router.urls)),
    path('teacher-courses/', views.TeacherCoursesDetailView.as_view()),
    path('teacher-students/', views.TeacherStudentsList.as_view()),

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

    path('users/', users_views.UserDetailView.as_view(), name="api_users_list"),
    path('users/<int:id>/', users_views.UserDetailView.as_view(), name="api_user_detail"),
    #path('users/<int:pk>/', users_views.UserDetailView.as_view()),
    #path('users/<int:pk>/', users_views.UserDetailView.as_view()),
    path('email-exist/', users_views.EmailExist),

    path('subjects/', course_views.SubjectDetailView.as_view()),
    path('subjects/<int:pk>/', course_views.SubjectDetailView.as_view()),
    path('courses_time_logs/', course_views.CourseTimeLogDetailView.as_view()),
    path('add-content-progress/', course_views.AddContentProgressApiView.as_view()),
    path('enable-content-progress/', course_views.UpdateHasProgress),
    path('course-features/', course_views.CourseFeatureApiView.as_view()),
    path('course-features/<int:pk>/', course_views.CourseFeatureApiView.as_view()),
    path('course-evaluation/', course_views.CourseEvaluationApiView.as_view()),
    #path('course-assess-rating/', course_views.CourseRatingApiView.as_view(), name='api_course_assess_rating'),
    path('course-price/<int:pk>/', course_views.CoursePriceApiView.as_view()),
    path('course-image/<int:pk>/', course_views.CourseImageApiView.as_view()),
    path('course-video/<int:pk>/', course_views.CourseVideoApiView.as_view()),
    path('update-course-quiz/', course_views.UpdateQuizApiView.as_view()),

    path('external-video-room/', chat_views.ExternalVideoRoomDetailView.as_view()),
    path('external-video-room/<int:pk>/',
         chat_views.ExternalVideoRoomDetailView.as_view()),

    path('attendance/', attendance_views.AttendanceApiView.as_view()),
    path('attendance/<int:pk>/', attendance_views.AttendanceApiView.as_view()),
    path('approve-attendance/', attendance_views.ApproveAttendance),

    path('student-history/', student_views.StudentsHistoryApiView.as_view()),
    path('quiz-details/', student_views.QuizApiView.as_view()),

    path('orders/', cart_views.OrderApiView.as_view()),
    path('packages/', cart_views.PackageApiView.as_view()),
    path('packages/<int:pk>/', cart_views.PackageApiView.as_view()),
    path('package-courses/', cart_views.PackageCourseApiView.as_view()),
    path('package-courses/<int:pk>/', cart_views.PackageCourseApiView.as_view()),
    path('package-subjects/', cart_views.PackageSubjectApiView.as_view()),

    path('quiz/', quiz_views.QuizApiView.as_view()),

    path('tags/', tag_views.TagApiView.as_view()),
    
    path('update-module-quiz/', course_module_views.UpdateQuizApiView.as_view()),

    path('conversations/', chat_views.ConversationDetailView.as_view(), name='api_conversations'),
    path('messages/', chat_views.MessageList.as_view(),name='api_messages'),

#     path('conversations/<int:pk>/', views.ConversationDetailView.as_view()),
#     path('conversation-members/', views.ConversationMembersList.as_view()),
#     path('conversation-members/<int:pk>/',
#          views.ConversationMembersList.as_view()),
#     ,

    path('save-base64/', views.SaveBase64ImageView),

    path('', include(router.urls)),
]
