from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.db import models
from django.db.models import Func
from django.db.models import Sum

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from app_cart.models import Payment
from app_api_v2.serializers import cart_serializers


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class PaymentView(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def get_earnings(self, request):

        queryset = Payment.objects

        year = request.query_params.get('year')
        if year:
            queryset = queryset.filter(created__year=year)
        
        queryset = (queryset.annotate(month=Month('created')).values(
            'month').annotate(total=Sum('amount_paid')).order_by())
        
        serializer = cart_serializers.PaymentAmountGroupSerializer(
            queryset, many=True)
        return Response(serializer.data)
