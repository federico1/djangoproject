from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from courses.models import Subject
from app_api_v2.serializers.subject_serializers import SubjectCreateSerializer

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000



class SubjectView(viewsets.GenericViewSet):
    page_size = 10
    serializer_class = SubjectCreateSerializer

    def list(self, request):
        queryset = Subject.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = self.page_size
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = SubjectCreateSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)