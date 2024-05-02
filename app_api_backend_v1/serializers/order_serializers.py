
from rest_framework import serializers
from app_cart.models import Order, Item, Payment
from courses.models import Course
from students.models import User


class CourseCoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'slug', 'subject', 'title', 'discounted_price', 'price']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('course', 'price', 'sub_total', 'qty')

    def to_representation(self, instance):
        self.fields['course'] = CourseCoreSerializer(read_only=True)
        return super(ItemSerializer, self).to_representation(instance)


class UserCoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'image']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('gateway', 'info', 'total_price', 'amount_paid')


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    payments = PaymentSerializer(many=True)
    user = UserCoreSerializer(many=False)

    class Meta:
        model = Order
        fields = ('id','ref_id', 'user', 'total_amount', 'status', 'created', 'items', 'payments')
