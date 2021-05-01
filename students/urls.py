from django.urls import path, include
from .views import students, classroom, teachers
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('classroom/', classroom.index, name='classroom'),
    path('register/student/', students.StudentRegistrationView.as_view(),
         name='student_registration'),
    path('enroll-course/', students.StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),
    path('courses/', students.StudentCourseListView.as_view(),
         name='student_course_list'),
    path('course/<int:pk>/', cache_page(60 * 15)
         (students.StudentCourseDetailView.as_view()), name='student_course_detail'),
    path('course/<int:pk>/<int:module_id>/', cache_page(60 * 15)
         (students.StudentCourseDetailView.as_view()), name='student_course_detail_module'),

    path('student/quiz/', students.QuizListView.as_view(),
         name='student_quiz_list'),

    path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
    path('student/quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
    path('student/quiz/result/<int:pk>/',
         students.quiz_result, name='quiz_result'),
    path('quiz/reset/<int:pk>/', students.quiz_reset, name='quiz_reset'),
    path('student/recommended-courses/', students.student_recommendation_list,
         name='student_recommendation_list'),
    path('enroll-course-quick/<int:pk>/',
         students.quick_course_enrol, name='quick_enroll'),

    path('register/teacher/', teachers.TeacherRegistrationView.as_view(),
         name='teacher_registration'),
    path('quiz/', teachers.TeacherQuizListView.as_view(),
         name='teacher_quiz_change_list'),
    path('quiz/add/', teachers.QuizCreateView.as_view(), name='teacher_add_quiz'),
    path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(),
         name='teacher_update_quiz'),
    path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(),
         name='teacher_delete_quiz'),
    path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(),
         name='teacher_quiz_results'),
    path('quiz/<int:pk>/question/add/',
         teachers.question_add, name='teacher_add_question'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/',
         teachers.question_change, name='teacher_change_question'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/delete/',
         teachers.QuestionDeleteView.as_view(), name='teacher_delete_question'),
    path('uploadfile', students.file_upload, name='upload-file'),

    path('course/certificate/<int:pk>/', cache_page(60 * 15)
         (students.CourseCertificateDetailView.as_view()), name='student_course_certificate'),
    path('course/certificate-template/<int:pk>/', cache_page(60 * 15)
         (students.CertificateTemplateDetailView.as_view()), name='student_course_certificate_template'),
    path('course/<int:pk>/certificate/download',
         students.download_certificate, name='student_download_certificate'),
    path('evaluate/<pk>',
         students.EvaluateDetailView.as_view(),
         name='course_evaluate'),
    path('course/assessment/<pk>',
         students.CourseAssessmentDetailView.as_view(),
         name='course_assessment'),
]
