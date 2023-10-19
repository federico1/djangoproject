from rest_framework import serializers


class PaymentAmountGroupSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    total = serializers.DecimalField(decimal_places=2, max_digits=100000)


class OrderGroupCountSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    total = serializers.IntegerField()