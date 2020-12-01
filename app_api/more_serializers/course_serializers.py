from rest_framework import serializers
from courses.models import Subject, Course, CourseTimeLog
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
                  'overview', 'total_modules', 'owner']

    def to_representation(self, instance):
        self.fields['owner'] = UserSerializer(read_only=True)
        self.fields['subject'] = SubjectSerializer(read_only=True)
        return super(CourseSerializer, self).to_representation(instance)



class CourseTimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTimeLog
        fields = '__all__'