from rest_framework import serializers
from app_chat.models import Conversation, Message, ConversationMember, VideoRoom, VideoParticipant, Notification, ParticipantLog, VideoCourses
from courses.models import Course
from students.models import User


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class ConversationMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationMember
        fields = ('id', 'member', 'conversation')
        read_only_fields = ('created', )

    def to_representation(self, instance):
        self.fields['member'] = UserSerializer(read_only=True)
        self.fields['conversation'] = ConversationSerializer(read_only=True)
        return super(ConversationMemberSerializer, self).to_representation(instance)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'content', 'sent', 'conversation', 'created')

    def to_representation(self, instance):
        self.fields['sent'] = UserSerializer(read_only=True)
        self.fields['conversation'] = ConversationSerializer(read_only=True)
        return super(MessageSerializer, self).to_representation(instance)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.cell_number = validated_data.get('cell_number', instance.cell_number)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.image = validated_data.get('image', instance.image)

        instance.save()

        return instance

    def to_representation(self, instance):
        return super(UserSerializer, self).to_representation(instance)

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

        self.fields.pop('user_permissions')
        self.fields.pop('password')
        self.fields.pop('groups')


class VideoCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCourses
        fields = ('id', 'created', 'room', 'course')

    def to_representation(self, instance):
        #self.fields['room'] =  VideoRoomSerializer(read_only=True)
        self.fields['course'] = CourseSerializer(read_only=True)
        return super(VideoCoursesSerializer, self).to_representation(instance)


class VideoRoomSerializer(serializers.ModelSerializer):
    courses = VideoCoursesSerializer(many=True, read_only=True)
    start_date = serializers.DateField(
        format=None, input_formats=None, allow_null=True)

    class Meta:
        model = VideoRoom
        fields = ('id', 'title', 'details', 'info', 'created', 'owner', 'status', 'participant_count',
                  'participant_max', 'start_date', 'start_time', 'is_deleted', 'courses')

    def to_representation(self, instance):
        self.fields['owner'] = UserSerializer(read_only=True)
        return super(VideoRoomSerializer, self).to_representation(instance)


class VideoParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoParticipant
        fields = ('id', 'member', 'room', 'is_approved')
        read_only_fields = ('created', )

    def to_representation(self, instance):
        self.fields['member'] = UserSerializer(read_only=True)
        self.fields['room'] = VideoRoomSerializer(read_only=True)
        return super(VideoParticipantSerializer, self).to_representation(instance)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['owner'] = UserSerializer(read_only=True)
        self.fields['receiver'] = UserSerializer(read_only=True)
        return super(NotificationSerializer, self).to_representation(instance)


class ParticipantLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantLog
        fields = ('id', 'participant', 'room')
        read_only_fields = ('created', )

    def to_representation(self, instance):
        self.fields['participant'] = UserSerializer(read_only=True)
        self.fields['room'] = VideoRoomSerializer(read_only=True)
        return super(ParticipantLogSerializer, self).to_representation(instance)
