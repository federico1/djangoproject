from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from courses.models import AssessRating
from ..serializers.course_rating_serializers import CourseAssessmentGroupByCourseSerializer, CourseAssessmentsByCourseSerializer

from django.db.models import Count


class AssessRatingView(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def get_courses_ids(self, request):
        snippets = AssessRating.objects.values(
            'course').annotate(ratings_count=Count('course')).order_by('-ratings_count')
        serializes = CourseAssessmentGroupByCourseSerializer(
            snippets, many=True)
        return Response(serializes.data)

    @action(detail=False, methods=['get'])
    def get_course_ratings(self, request):
        course_id = int(self.request.query_params.get('course_id'))
        snippets = AssessRating.objects.filter(
            course_id=course_id)
        serializes = CourseAssessmentsByCourseSerializer(
            snippets, many=True)
        return Response(serializes.data)
