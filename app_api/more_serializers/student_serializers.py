from rest_framework import serializers
from students.models import User, SSTCard
from app_api.serializers import UserSerializer


class SSTCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSTCard
        fields = ['card_id', 'card_type', 'qr_code', 'renew_status', 'issued', 'expired']

    def to_representation(self, instance):
        self.fields['student'] = UserSerializer(read_only=True)
        return super(SSTCardSerializer, self).to_representation(instance)


# class StudentRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'cell_number', 'email', 'first_name', 'last_name', 'address', 'image')

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)

#         user.save()
#         return user

#     def update(self, instance, validated_data):
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.cell_number = validated_data.get('cell_number', instance.cell_number)
#         instance.email = validated_data.get('email', instance.email)
#         instance.address = validated_data.get('address', instance.address)
#         instance.image = validated_data.get('image', instance.image)

#         instance.save()

#         return instance

#     def to_representation(self, instance):
#         return super(StudentRegisterSerializer, self).to_representation(instance)

#     def __init__(self, *args, **kwargs):
#         super(UserSerializer, self).__init__(*args, **kwargs)

#         self.fields.pop('user_permissions')
#         self.fields.pop('password')
#         self.fields.pop('groups')
