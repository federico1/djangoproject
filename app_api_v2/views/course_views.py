from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.db import models
from django.db.models import Func, Count


from courses.models import Enrollments
from app_api_v2.serializers import course_serializers

class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()

class Year(Func):
    function = 'EXTRACT'
    template = '%(function)s(YEAR from %(expressions)s)'
    output_field = models.IntegerField()


class EnrollmentView(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def get_group_count(self, request):

        queryset = Enrollments.objects

        year = request.query_params.get('year')
        plan = request.query_params.get('plan')

        if year:
            queryset = queryset.filter(created__year=year)

        if plan and plan == 'free':
            queryset = queryset.filter(course__is_free=1)

        if plan and plan == 'paid':
            queryset = queryset.filter(course__is_free=0)

        queryset = queryset.annotate(year=Year('created'), month=Month(
            'created'),).values('year', 'month').annotate(total=Count('id')).order_by()
        
        serializer = course_serializers.EnrollmentGroupCountSerializer(
            queryset, many=True)
        return Response(serializer.data)
