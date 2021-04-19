from rest_framework import serializers
from courses.models import Subject, Course, CourseTimeLog, CourseProgress, CourseFeature, Attendance, Enrollments
from students.models import User
from app_api.serializers import UserSerializer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollments
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    total_modules = serializers.IntegerField()

    course_enrolled = EnrollmentSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'slug', 'subject', 'title',
                  'overview', 'total_modules', 'owner', 'course_enrolled']

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


# class StudentCourseSerializer(serializers.Serializer):
#     student = serializers.IntegerField(required=True)
#     course = serializers.IntegerField(required=True)

#     def create(self, validated_data):
#         course_id = validated_data.pop('course')
#         student_id = validated_data.pop('student')

#         Course.objects.get(pk=course_id).students.add(student_id)

#         return {'student':student_id, 'course':course_id}


class CourseFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFeature
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


