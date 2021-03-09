from rest_framework import serializers
from courses.models import Subject, Course, CourseTimeLog, CourseProgress, CourseFeature
from students.models import User
from app_api.serializers import UserSerializer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    total_modules = serializers.IntegerField()

    class Meta:
        model = Course
        fields = ['id', 'slug', 'subject', 'title',
                  'overview', 'total_modules', 'owner', 'students']

    def to_representation(self, instance):
        self.fields['owner'] = UserSerializer(read_only=True)
        self.fields['subject'] = SubjectSerializer(read_only=True)
        return super(CourseSerializer, self).to_representation(instance)


class CourseTimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTimeLog
        fields = '__all__'


class CourseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseProgress
        fields = '__all__'


class StudentCourseSerializer(serializers.Serializer):
    student = serializers.IntegerField(required=True)
    course = serializers.IntegerField(required=True)

    def create(self, validated_data):
        course_id = validated_data.pop('course')
        student_id = validated_data.pop('student')

        Course.objects.get(pk=course_id).students.add(student_id)

        return {'student':student_id, 'course':course_id}


class CourseFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFeature
        fields = '__all__'