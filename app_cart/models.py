from django.db import models
from django.conf import settings
from courses.models import Course


ORDER_STATUS = [
    (0, 'Pending'),
    (1, 'Active'),
    (2, 'Rejected'),
    (3, 'Cancelled'),
]

PAYMENT_STATUS = [
    (0, 'Approved'),
    (1, 'Rejected'),
]


class Order(models.Model):
    ref_id = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                             related_name='orders',
                             on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.IntegerField(choices=ORDER_STATUS, default=0)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=0)

    class Meta:
        ordering = ['ref_id']

    def __str__(self):
        return self.ref_id


class Item(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, related_name='order_items',  on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    sub_total = models.DecimalField(max_digits=5, decimal_places=2)
    qty = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.price


class Payment(models.Model):
    order = models.ForeignKey(
        Order, related_name='payments', on_delete=models.CASCADE)
    gateway = models.CharField(max_length=200)
    info = models.TextField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.IntegerField(
        choices=PAYMENT_STATUS, default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.order
