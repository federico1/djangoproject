from rest_framework import serializers
from courses.models import AssessRating
from app_api_admin_v1.serializers.order_serializers import UserCoreSerializer


class CourseAssessmentGroupByCourseSerializer(serializers.Serializer):
    course = serializers.IntegerField()
    ratings_count = serializers.IntegerField()


class CourseAssessmentsByCourseSerializer(serializers.ModelSerializer):
    student = UserCoreSerializer(many=False)

    class Meta:
        model = AssessRating
        fields = ('student', 'course', 'key_name', 'key_value', 'created')
