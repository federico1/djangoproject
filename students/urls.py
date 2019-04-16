from django.urls import path, include
from .views import students, classroom, teachers
from django.views.decorators.cache import cache_page


urlpatterns = [
     path('classroom/', classroom.index, name='classroom'),

    path('register/student/', students.StudentRegistrationView.as_view(), name='student_registration'),
    path('enroll-course/', students.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('courses/', students.StudentCourseListView.as_view(), name='student_course_list'),
    path('course/(?P<pk>\d+)/', cache_page(60*15)(students.StudentCourseDetailView.as_view()), name='student_course_detail'),
    path('course/(?P<pk>\d+)/(?P<module_id>\d+)/', cache_page(60*15)(students.StudentCourseDetailView.as_view()), name='student_course_detail_module'),
    path('student/quiz/', students.QuizListView.as_view(), name='student_quiz_list'),
    path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
    path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
    path('student/quiz/(?P<pk>\d+)/', students.take_quiz, name='take_quiz'),
    path('student/recommended-courses/', students.student_recommendation_list, name='student_recommendation_list'),

    path('register/teacher/', teachers.TeacherRegistrationView.as_view(), name='teacher_registration'),
    path('quiz/', teachers.TeacherQuizListView.as_view(), name='teacher_quiz_change_list'),
    path('quiz/add/', teachers.QuizCreateView.as_view(), name='teacher_add_quiz'),
    path('quiz/(?P<pk>\d+)/', teachers.QuizUpdateView.as_view(), name='teacher_update_quiz'),
    path('quiz/(?P<pk>\d+)/delete/', teachers.QuizDeleteView.as_view(), name='teacher_delete_quiz'),
    path('quiz/(?P<pk>\d+)/results/', teachers.QuizResultsView.as_view(), name='teacher_quiz_results'),
    path('quiz/(?P<pk>\d+)/question/add/', teachers.question_add, name='teacher_add_question'),
    path('quiz/(?P<quiz_pk>\d+)/question/(?P<question_pk>\d+)/', teachers.question_change, name='teacher_change_question'),
    path('quiz/(?P<quiz_pk>\d+)/question/(?P<question_pk>\d+)/delete/', teachers.QuestionDeleteView.as_view(), name='teacher_delete_question'),
 ]
