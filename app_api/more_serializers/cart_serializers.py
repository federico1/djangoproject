from rest_framework import serializers
from app_cart.models import Order, Item, Payment, Package, PackageCourse
from .course_serializers import CourseCoreSerializer
from students.models import User
from courses.models import Enrollments


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('course', 'price', 'sub_total', 'qty')

    def to_representation(self, instance):
        self.fields['course'] = CourseCoreSerializer(read_only=True)
        return super(ItemSerializer, self).to_representation(instance)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('gateway', 'info', 'total_price', 'amount_paid')


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    payments = PaymentSerializer(many=True)

    class Meta:
        model = Order
        fields = ('ref_id', 'user', 'total_amount', 'status', 'items', 'payments')

    def create(self, validated_data):

        items_data = validated_data.pop('items')
        payments_data = validated_data.pop('payments')

        payment_status_id = Payment.PENDING
        order_status_id = Order.PENDING

        if len(payments_data) > 0 and payments_data[0]['gateway'] == 'paypal':
            payment_status_id = Payment.COMPLETED
            order_status_id = Order.APPROVED

        order = Order.objects.create(status=order_status_id, **validated_data)

        for item_data in items_data:
            
            enrollment = None

            if not Enrollments.objects.filter(course=item_data['course'], user=order.user).exists():
                enrollment = Enrollments.objects.create(
                course=item_data['course'], user=order.user, price=item_data['price'], created_by=self.context['request'].user.id)

            Item.objects.create(order=order, enrollment = enrollment, **item_data)
        
        for item_data in payments_data:
            Payment.objects.create(order=order, status=payment_status_id, **item_data)

        return order


class PackageCourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PackageCourse
        fields = ('id', 'course', 'package', 'course_id')



    def to_representation(self, instance):
        self.fields['course'] = CourseCoreSerializer(read_only=True)
        return super(PackageCourseSerializer, self).to_representation(instance)


class PackageSerializer(serializers.ModelSerializer):
    courses = PackageCourseSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ('id', 'name', 'price', 'sort_order', 'created', 'is_deleted', 'courses','subjects')


