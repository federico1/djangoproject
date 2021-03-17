from rest_framework import serializers
from app_chat.models import ExternalVideoRoom
from students.models import User
from app_api.serializers import UserSerializer


class ExternalVideoRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalVideoRoom
        fields = '__all__'