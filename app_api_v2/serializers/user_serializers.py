from rest_framework import serializers

from students.models import User


class UserBasicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image')
