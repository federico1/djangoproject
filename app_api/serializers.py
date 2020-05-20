from rest_framework import serializers
from app_chat.models import Conversation, Message, ConversationMember
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
        self.fields['member'] =  UserSerializer(read_only=True)
        self.fields['conversation'] =  ConversationSerializer(read_only=True)
        return super(ConversationMemberSerializer, self).to_representation(instance)

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'content', 'sent', 'conversation', 'created')

    def to_representation(self, instance):
        self.fields['sent'] =  UserSerializer(read_only=True)
        self.fields['conversation'] =  ConversationSerializer(read_only=True)
        return super(MessageSerializer, self).to_representation(instance)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'