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
from django.db.models import Count

from courses.models import Subject, Course, CourseTimeLog, CourseProgress, Content, CourseFeature, Enrollments, \
    Evaluation

from app_api.more_serializers.course_serializers import SubjectSerializer, CourseSerializer, \
    CourseTimeLogSerializer, CourseProgressSerializer, CourseFeatureSerializer, EnrollmentSerializer, \
    EvaluationSerializer

from students.models import User
from django.conf import settings

from datetime import datetime


class SubjectDetailView(APIView):

    def get_object(self, pk):
        try:
            return Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        snippets = Subject.objects
        serializer = SubjectSerializer(snippets, many=True)

        return Response(serializer.data)


class CourseViewset(viewsets.ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request):

        snippets = self.queryset

        c_order = request.query_params.get('order')
        c_limit = request.query_params.get('limit')

        order_field = '-id'

        if c_order is not None and c_order == 'asc':
            order_field = 'id'

        if c_limit is not None:
            snippets = snippets.order_by(order_field)[:int(c_limit)]

        snippets = snippets.annotate(total_modules=Count('modules'))

        serializer = CourseSerializer(snippets, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        snippets = self.queryset.filter(id=pk)

        snippets = snippets.annotate(total_modules=Count('modules'))

        serializer = CourseSerializer(snippets, many=True)

        return Response(serializer.data)


class CourseTimeLogDetailView(APIView):

    def get(self, request, format=None):

        course_id = request.query_params.get('course')

        snippets = CourseTimeLog.objects.filter(
            user=request.user, course_id=course_id)
        serializer = CourseTimeLogSerializer(snippets, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CourseTimeLogSerializer(data=request.data)

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
        serializer = CourseProgressSerializer(data=request.data)
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

        snippets = Enrollments.objects

        if course_id is not None:
            snippets = snippets.filter(course_id=course_id)

        serializer = EnrollmentSerializer(snippets, many=True)

        return Response(serializer.data)

    def create(self, request):

        serializer = EnrollmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def set_completed(self, request, pk=None):
        snippet = self.get_object(pk)
        snippet.is_completed = request.data['status']
        snippet.completed_date = datetime.now()
        snippet.save()

        serializer = EnrollmentSerializer(snippet)

        return Response(serializer.data)


class CourseFeatureApiView(APIView):

    def get(self, request, format=None):
        snippets = CourseFeature.objects.all()

        course_id = request.query_params.get('course')

        if course_id:
            snippets = CourseFeature.objects.filter(course_id=course_id)

        serializer = CourseFeatureSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CourseFeatureSerializer(data=request.data)

        if serializer.is_valid():

            course_id = serializer.validated_data['course']

            snippets = CourseFeature.objects.filter(course_id=course_id)

            for item in snippets:
                item.delete()

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class CourseEvaluationApiView(APIView):

    def get(self, request, format=None):
        snippets = Evaluation.objects.all()
        serializer = EvaluationSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EvaluationSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
