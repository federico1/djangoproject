from rest_framework import serializers

class EnrollmentGroupCountSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    total = serializers.IntegerField()