from django.db import models
from django.conf import settings
from courses.models import Course, Subject, Enrollments


class Order(models.Model):

    PENDING = 0
    APPROVED = 1
    REJECTED = 2
    CANCEL = 3

    ORDER_STATUS = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (CANCEL, 'Cancelled'),
    ]

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
        Course, related_name='order_items', on_delete=models.CASCADE)
    enrollment = models.ForeignKey(
        Enrollments, related_name='order_item', on_delete=models.DO_NOTHING, null=True, blank=True)
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
    PENDING = 0
    COMPLETED = 1
    REJECTED = 2

    PAYMENT_STATUS = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (REJECTED, 'Rejected'),
    ]

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

    DEFAULT = 0
    COURSES_BUNDLE = 1
    SUBJECT_LINKED = 2
    FREE_CREDITS = 3

    PACKAGE_TYPE = [
        (DEFAULT, 'Default'),
        (COURSES_BUNDLE, 'Courses Bundle'),
        (SUBJECT_LINKED, 'Subject Linked'),
        (FREE_CREDITS, 'Free Credits'),
    ]

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    sort_order = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=0)
    free_credits = models.IntegerField(default=0)
    package_type = models.IntegerField(
        choices=PACKAGE_TYPE, default=DEFAULT)
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


class BusinessUserCredit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # Ensure only business users can have credits
        limit_choices_to={'is_business': True},
        related_name='business_credits'
    )
    order = models.ForeignKey(
        Order, related_name='credits', on_delete=models.DO_NOTHING, null=True)
    credits_purchased = models.IntegerField(default=0)
    credits_remaining = models.IntegerField(
        default=0)  # Remaining credits from this batch
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.credits_remaining} credits remaining for {self.user.username}"

    class Meta:
        verbose_name = "Business User Credit"
        verbose_name_plural = "Business User Credits"
