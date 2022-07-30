from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from app_api.more_serializers.quiz_serializers import QuizSerializer
from courses.models import Content, Image, Module, Subject, Course, CourseTimeLog, CourseProgress, \
    CourseFeature, Attendance, Enrollments, Evaluation, AssessRating, Text, File, Video, IFrame
from students.models import User
from app_api.serializers import UserSerializer


class SubjectSerializer(serializers.ModelSerializer):
    
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug', 'course_count', 'page_title', 'page_details', 'meta_title', 'meta_tags', 'meta_description', 'video_link']
    
    def get_course_count(self, obj):
        return obj.courses.count()


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollments
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super(EnrollmentSerializer, self).to_representation(instance)


class EnrollmentP2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollments
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['course'] = CourseCoreSerializer(read_only=True)
        return super(EnrollmentP2Serializer, self).to_representation(instance)


class CourseSerializer(serializers.ModelSerializer):
    total_modules = serializers.IntegerField()
    course_enrolled = EnrollmentSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'slug', 'subject', 'title',
                  'overview', 'total_modules', 'owner', 'course_enrolled','price','discounted_price', 'is_free']

    def to_representation(self, instance):
        self.fields['owner'] = UserSerializer(read_only=True)
        self.fields['subject'] = SubjectSerializer(read_only=True)
        return super(CourseSerializer, self).to_representation(instance)


class CourseCoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'slug', 'subject', 'title', 'overview', 'quiz', 'price']


class CoursePriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'price', 'is_free', 'discounted_price']


class CourseTimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTimeLog
        fields = '__all__'


class CourseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseProgress
        fields = '__all__'


class CourseImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'image',]


class CourseFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFeature
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['student'] = UserSerializer(read_only=True)
        self.fields['course'] = CourseCoreSerializer(read_only=True)
        return super(EvaluationSerializer, self).to_representation(instance)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessRating
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['student'] = UserSerializer(read_only=True)
        self.fields['course'] = CourseCoreSerializer(read_only=True)
        return super(RatingSerializer, self).to_representation(instance)


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class IFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = IFrame
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class ContentObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        """
        Serialize bookmark instances using a bookmark serializer,
        and note instances using a note serializer.
        """
        if isinstance(value, Text):
            serializer = TextSerializer(value)
        elif isinstance(value, Image):
            serializer = ImageSerializer(value)
        elif isinstance(value, Video):
            serializer = VideoSerializer(value)
        elif isinstance(value, IFrame):
            serializer = IFrameSerializer(value)
        elif isinstance(value, File):
            serializer = FileSerializer(value)
        else:
             raise Exception('Unexpected type of content object')


        return serializer.data


class ContentSerializer(serializers.ModelSerializer):
    #content_type = ContentObjectRelatedField(read_only=True)
    item = ContentObjectRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['content_type', 'has_progress', 'object_id', 'order', 'item']

    def to_representation(self, instance):
        self.fields['quiz'] = QuizSerializer(read_only=True)
        return super(ContentSerializer, self).to_representation(instance)


class ModuleSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'quiz', 'contents']

    def to_representation(self, instance):
        self.fields['quiz'] = QuizSerializer(read_only=True)
        return super(ModuleSerializer, self).to_representation(instance)


class CourseDepthSerializer(serializers.ModelSerializer):
    course_enrolled = EnrollmentSerializer(many=True)
    modules = ModuleSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'slug', 'subject', 'title', 'mark_type' , 'overview', 'image', 'video',
         'is_free', 'is_approved', 'is_deleted', 'price','discounted_price', 'created' , 
         'owner', 'subject', 'quiz', 'course_enrolled', 'modules' ]

    def to_representation(self, instance):
        self.fields['owner'] = UserSerializer(read_only=True)
        self.fields['subject'] = SubjectSerializer(read_only=True)
        self.fields['quiz'] = QuizSerializer(read_only=True)
        return super(CourseDepthSerializer, self).to_representation(instance)

