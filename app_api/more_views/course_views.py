from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Count

from courses.models import Subject, Course, CourseTimeLog, CourseProgress
from app_api.more_serializers.course_serializers import *

from students.models import User
from django.conf import settings


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


class CourseDetailView(APIView):

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        snippets = Course.objects

        c_order = request.query_params.get('order')
        c_limit = request.query_params.get('limit')

        order_field = '-id';

        if c_order is not None and c_order == 'asc':
            order_field = 'id'
        
        if c_limit is not None:
            snippets = snippets.order_by(order_field)[:int(c_limit)]
        
        snippets = snippets.annotate(total_modules=Count('modules'))

        serializer = CourseSerializer(snippets, many=True)

        return Response(serializer.data)


class CourseTimeLogDetailView(APIView):

    def get(self, request, format=None):

        course_id = request.query_params.get('course')

        snippets = CourseTimeLog.objects.filter(user=request.user, course_id=course_id)
        serializer = CourseTimeLogSerializer(snippets, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CourseTimeLogSerializer(data=request.data)

        if serializer.is_valid():
            
            course = serializer.validated_data['course']
            snippets = CourseTimeLog.objects.filter(user=request.user, course=course)

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


class CourseProgressApiView(APIView):
   
    def get(self, request, format=None):
        snippets = CourseProgress.objects.all()
        serializer = CourseProgressSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CourseProgressSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.validated_data['content']

            snippets = CourseProgress.objects.filter(user=request.user, content=content)

            if snippets.count() <= 0:
                serializer.save(user=request.user)
            else:
                snippets.first().save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)