from rest_framework import serializers
from app_chat.models import ExternalVideoRoom, Conversation, ConversationMember, Message
from students.models import User
from app_api.serializers import UserSerializer


class ExternalVideoRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalVideoRoom
        fields = '__all__'


class ConversationMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationMember
        fields = ('id', 'member', 'conversation')
        read_only_fields = ('created', )

    def to_representation(self, instance):
        # self.fields['member'] = UserSerializer(read_only=True)
        # self.fields['conversation'] = ConversationSerializer(read_only=True)
        return super(ConversationMemberSerializer, self).to_representation(instance)


class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = ('id','title', 'created', 'course', 'is_deleted')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'content', 'sent', 'conversation', 'created')

    def to_representation(self, instance):
        self.fields['sent'] = UserSerializer(read_only=True)
        self.fields['conversation'] = ConversationSerializer(read_only=True)
        return super(MessageSerializer, self).to_representation(instance)
