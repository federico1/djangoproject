from rest_framework import serializers
from app_cart.models import Package


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'
