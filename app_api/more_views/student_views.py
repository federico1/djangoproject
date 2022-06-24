
from operator import mod
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app_api.more_serializers.quiz_serializers import QuizSerializer
from students.models import User, Quiz
from courses.models import Course, Enrollments
from django.core import serializers


class CourseProgressView(APIView):

    def get(self, request, format=None):

        student_id = request.query_params.get('student')
        course_id = request.query_params.get('course')

        user = User.objects.get(pk=student_id)
        enrolled = user.my_enrolled.get(course_id=course_id)
        course = enrolled.course
        modules_list = course.modules.all().order_by('order')
        taken_quizzes = list(
            user.taken_quizzes.values_list('quiz_id', flat=True))
        progress_list = user.courses_progress.all()
        course_details = []
        total_lessons = 0
        completed_lessons = 0

        for module in modules_list:
            module_item = {'module': {'id': module.id, 'title': module.title},
                           'contents': [],
                           'quiz': None}

            for content in module.contents.order_by('order'):

                c_count = progress_list.filter(
                    content_id=content.id, is_completed=True).count()

                item_obj = {'type': 'content',
                            'id': content.id,
                            'title': content.item.title,
                            'complete': True if c_count > 0 else False}

                module_item['contents'].append(item_obj)

                total_lessons = total_lessons+1

                if c_count > 0:
                    completed_lessons = completed_lessons+1

                # item_obj = {'type': 'content',
                #             'object': serializers.serialize('json', [content.item, ]),
                #             'module': serializers.serialize('json', [module, ]),
                #             'complete': True if c_count > 0 else False}

            if module.quiz is not None:

                if module.quiz.questions.count() > 0:
                    score = 0
                    item_obj = {'type': 'quiz',
                                'name': module.quiz.name,
                                'score': score,
                                'complete': True if module.quiz.id in taken_quizzes else False}
                    module_item['quiz'] = item_obj
                    total_lessons = total_lessons+1
                    if item_obj['complete'] == True:
                        completed_lessons = completed_lessons+1

            course_details.append(module_item)

            response = {
                'summary': {
                    'total_lessons': total_lessons,
                    'completed_lessons': completed_lessons
                },
                'data': course_details}

        return Response(response)


class QuizApiView(APIView):

    def get(self, request, format=None):

        user = request.user

        quiz_id = request.query_params.get('id')

        snippets = Quiz.objects.filter(id=quiz_id).first()

        # if quiz_id is not None:
        #     snippets = snippets.filter(id=quiz_id)

        serializer = QuizSerializer(snippets)

        return Response(serializer.data)
