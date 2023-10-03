from rest_framework import serializers
from app_chat.models import Conversation, Message, ConversationMember, Notification
from courses.models import Course
from students.models import User


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    enrolled_count = serializers.IntegerField(source='my_enrolled.count', read_only=True)
    class Meta:
        model = User
        fields = '__all__'
        extra_fields = ['enrolled_count']

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
        #self.fields.pop('password')
        self.fields.pop('groups')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['owner'] = UserSerializer(read_only=True)
        self.fields['receiver'] = UserSerializer(read_only=True)
        return super(NotificationSerializer, self).to_representation(instance)