from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, action
from django.http import Http404
from django.db.models import Count, Sum, Q, F
from datetime import datetime
from django.conf import settings
from django.core.cache import cache

from courses.models import Subject, Course, CourseTimeLog, CourseProgress, Content, CourseFeature, \
    Enrollments, Evaluation, AssessRating
from students.models import User
from app_api.more_serializers import course_serializers


class SubjectDetailView(APIView):

    def get_object(self, pk):
        try:
            return Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            raise Http404

    def get(self, request, format=None):

        snippets = cache.get('api_all_subjects')

        if not snippets:
            snippets = Subject.objects.all()
            # snippets = Subject.objects.annotate(free_count=(Count('id', filter=Q(courses__is_free=True))),
            #                                     paid_count=(Count('id', filter=Q(courses__is_free=False)))).order_by('-paid_count', 'free_count')
            cache.set('api_all_subjects', snippets)

        # paid_subjects = Subject.objects.filter(courses__is_free=False).annotate(courses_count=Count('id')).order_by('-courses_count')
        # free_subjects = Subject.objects.filter(courses__is_free=True).annotate(courses_count=Count('id')).order_by('-courses_count')

        serializer = course_serializers.SubjectSerializer(snippets, many=True)

        return Response(serializer.data)

    def put(self, request, format=None):
        subject_object = self.get_object(request.data['id'])
        serializer = course_serializers.SubjectSerializer(
            subject_object, data=request.data)

        if serializer.is_valid():
            serializer.save()
            cache.clear()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseViewset(viewsets.ModelViewSet):
    """ details of function"""

    queryset = Course.objects.all()
    serializer_class = course_serializers.CourseSerializer

    def list(self, request):

        snippets = self.queryset

        c_order = request.query_params.get('order')
        c_limit = request.query_params.get('limit')
        c_search_term = request.query_params.get('q')
        c_result_type = request.query_params.get('result_type')
        paid_only = request.query_params.get('paid_only')
        free_only = request.query_params.get('free_only')

        order_field = '-id'

        if c_order is not None and c_order == 'asc':
            order_field = 'id'

        if c_search_term is not None and c_search_term != '':
            snippets = snippets.filter(title__icontains=str(c_search_term))

        if paid_only is not None:
            snippets = snippets.filter(is_free=False)

        if free_only is not None:
            snippets = snippets.filter(is_free=True)

        if c_limit is not None:
            snippets = snippets.order_by(order_field)[:int(c_limit)]

        if c_result_type is not None and c_result_type == 'auto_search':
            serializer = course_serializers.CourseSearchSerializer(
                snippets, many=True)
            return Response(serializer.data)

        serializer = course_serializers.CourseCoreSerializer(
            snippets, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        snippets = self.queryset.filter(id=pk)

        snippets = snippets.annotate(total_modules=Count('modules'))

        serializer = course_serializers.CourseSerializer(snippets, many=True)

        return Response(serializer.data)

    def create(self, request):
        pass

    @action(detail=False)
    def depth(self, request):
        snippets = self.queryset

        c_order = request.query_params.get('order')
        c_limit = request.query_params.get('limit')

        order_field = '-id'

        if c_order is not None and c_order == 'asc':
            order_field = 'id'

        if c_limit is not None:
            snippets = snippets.order_by(order_field)[:int(c_limit)]

        snippets = snippets.annotate(total_modules=Count('modules'))

        serializer = course_serializers.CourseSerializer(snippets, many=True)

        return Response(serializer.data)


class CourseTimeLogDetailView(APIView):

    def get(self, request, format=None):

        course_id = request.query_params.get('course')

        snippets = CourseTimeLog.objects.filter(
            user=request.user, course_id=course_id)

        serializer = course_serializers.CourseTimeLogSerializer(
            snippets, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = course_serializers.CourseTimeLogSerializer(
            data=request.data)

        if serializer.is_valid():

            course = serializer.validated_data['course']
            snippets = CourseTimeLog.objects.filter(
                user=request.user, course=course)

            if snippets.count() > 0:
                time_object = snippets.last()
                time_object.total_seconds = request.data['total_seconds']
                time_object.save()
            else:
                serializer.save(user=request.user)

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class AddContentProgressApiView(APIView):

    def post(self, request, format=None):
        serializer = course_serializers.CourseProgressSerializer(
            data=request.data)
        if serializer.is_valid():
            content = serializer.validated_data['content']

            snippets = CourseProgress.objects.filter(
                user=request.user, content=content)

            if snippets.count() <= 0:
                serializer.save(user=request.user)
            else:
                snippets.first().save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentViewset(viewsets.ViewSet):

    def get_object(self, pk):
        try:
            return Enrollments.objects.get(pk=pk)
        except Enrollments.DoesNotExist:
            raise Http404

    def list(self, request):

        course_id = request.query_params.get('course')
        student_id = request.query_params.get('student')

        snippets = Enrollments.objects

        if course_id is not None:
            snippets = snippets.filter(course_id=course_id)

        if student_id is not None:
            snippets = snippets.filter(user_id=student_id)

        serializer = course_serializers.EnrollmentSerializer(
            snippets, many=True)

        return Response(serializer.data)

    def create(self, request):
        data = request.data

        if 'user' not in data:
            data['user'] = self.request.user.id

        course = Course.objects.get(pk=request.data['course'])

        data['created_by'] = self.request.user.id

        if course.is_free == True:
            data['price'] = 0
        else:
            data['price'] = course.discounted_price if course.discounted_price > 0 else course.price

        serializer = course_serializers.EnrollmentSerializer(data=data)

        if request.user.is_authenticated and request.user.is_student == True and serializer.is_valid():

            if course.is_free == False:
                return Response(serializer.data, status=status.HTTP_502_BAD_GATEWAY)

            if not Enrollments.objects.filter(course=request.data['course'], user=self.request.user).exists():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_226_IM_USED)
        # elif request.user.is_superuser == True and serializer.is_valid():

        #     if not Enrollments.objects.filter(course=request.data['course'], user=request.data['user']).exists():

        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     else:
        #         return Response(serializer.data, status=status.HTTP_226_IM_USED)

        serializer.is_valid()

        return Response(serializer.errors, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    @action(detail=True, methods=['post'])
    def set_completed(self, request, pk=None):
        snippet = self.get_object(pk)
        snippet.is_completed = request.data['status']
        snippet.completed_date = datetime.now()
        snippet.save()

        serializer = course_serializers.EnrollmentSerializer(snippet)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def force_remove(self, request, pk=None):
        snippet = self.get_object(pk)
        snippet.delete()
        serializer = course_serializers.EnrollmentSerializer(snippet)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_list(self, request, pk=None):

        if request.user.is_authenticated:
            snippets = Enrollments.objects.filter(user_id=request.user)
            serializer = course_serializers.EnrollmentCoreSerializer(
                snippets, many=True)
            return Response(serializer.data)

        return Response("AUTH", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class CourseFeatureApiView(APIView):

    def get(self, request, format=None):
        snippets = CourseFeature.objects

        course_id = request.query_params.get('course')

        if course_id:
            snippets = snippets.filter(course_id=course_id)

        serializer = course_serializers.CourseFeatureSerializer(
            snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = course_serializers.CourseFeatureSerializer(
            data=request.data)

        if serializer.is_valid():

            course_id = serializer.validated_data['course']
            snippets = CourseFeature.objects.filter(course_id=course_id)

            for item in snippets:
                item.delete()

            serializer.save()

            cache.clear()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoursePriceApiView(APIView):

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = course_serializers.CoursePriceSerializer(
            snippet, data=request.data)

        if serializer.is_valid():
            serializer.save()
            cache.clear()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseImageApiView(APIView):

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = course_serializers.CourseImageSerializer(
            snippet, data=request.data)

        if serializer.is_valid():
            serializer.save()
            cache.clear()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseVideoApiView(APIView):

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.video = request.POST['video']
        snippet.save()
        cache.clear()
        result = 1
        return Response(result)


class UpdateQuizApiView(APIView):

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        pk = request.POST['id']
        snippet = self.get_object(pk)
        snippet.quiz_id = request.POST['quiz_id']
        snippet.save()
        cache.clear()
        result = 1
        return Response(result)


class CourseEvaluationApiView(APIView):

    def get(self, request, format=None):
        snippets = Evaluation.objects.all()
        serializer = course_serializers.EvaluationSerializer(
            snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = course_serializers.EvaluationSerializer(data=request.data)
        serializer.initial_data["student"] = request.user.id

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseRatingViewSet(viewsets.ModelViewSet):

    queryset = AssessRating.objects.all()
    serializer_class = course_serializers.RatingSerializer

    def create(self, request, *args, **kwargs):

        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    @action(detail=False, methods=['get'])
    def is_rated(self, request):

        course = request.GET["course"]
        user = request.GET["user"]
        is_course_rated = AssessRating.objects.filter(
            course=course, student=user).exists()

        return Response(is_course_rated,
                        status=status.HTTP_200_OK)


class DumpCourse(APIView):

    def get(self, request, format=None):
        snippets = Course.objects
        serializer = course_serializers.CourseDepthSerializer(
            snippets, many=True)

        return Response(serializer.data)


@api_view(['GET', 'POST'])
def UpdateHasProgress(request):

    result = 0
    message = ""

    if request.method == 'POST':
        content = Content.objects.get(pk=request.data['id'])
        content.has_progress = request.data['progress']

        content.save()
        result = 1

    return Response({"message": message, "result": result})
