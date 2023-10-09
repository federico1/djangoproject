from django.db import models
from django.conf import settings
from courses.models import Course, Subject


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

    def get_order_slug(self):
        self.order.ref_id + "xx"

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
    
    def get_gateyway(self):
        if self.gateway == 'paypal':
            return "Paypal"
        elif self.gateway == 'Bank Tranfer':
            return 'Bank Tranfer'
        else:
            return self.gateway

    def __str__(self):
        return self.gateway


class Package(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    sort_order = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=0)
    subjects = models.ManyToManyField(Subject, blank=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class PackageCourse(models.Model):
    course = models.ForeignKey(Course,
                               related_name='package_courses',
                               on_delete=models.CASCADE)
    package = models.ForeignKey(Package,
                               related_name='courses',
                               on_delete=models.CASCADE)
   
    class Meta:
        ordering = ['package']

    def __str__(self):
        return '{}. {}'.format(self.course, self.package)
