from rest_framework import serializers

class PaymentAmountGroupSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    total = serializers.DecimalField(decimal_places=2, max_digits=100000)