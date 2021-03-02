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
