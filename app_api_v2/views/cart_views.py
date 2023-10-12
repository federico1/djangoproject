from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.db import models
from django.db.models import Func, Count, Sum

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from app_cart.models import Payment, Order
from app_api_v2.serializers import cart_serializers


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class Year(Func):
    function = 'EXTRACT'
    template = '%(function)s(YEAR from %(expressions)s)'
    output_field = models.IntegerField()


class OrderView(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def get_group_count(self, request):

        queryset = Order.objects

        year = request.query_params.get('year')
        if year:
            queryset = queryset.filter(created__year=year)

        queryset = queryset.annotate(year=Year('created'), month=Month(
            'created'),).values('year', 'month').annotate(total=Count('id')).order_by()

        serializer = cart_serializers.PaymentAmountGroupSerializer(
            queryset, many=True)
        return Response(serializer.data)


class PaymentView(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def get_amount_group_count(self, request):

        queryset = Payment.objects

        year = request.query_params.get('year')

        if year:
            queryset = queryset.filter(created__year=year)

        queryset = queryset.filter(status=1)

        queryset = queryset.annotate(year=Year('created'), month=Month(
            'created'),).values('year', 'month').annotate(total=Sum('amount_paid')).order_by()

        serializer = cart_serializers.PaymentAmountGroupSerializer(
            queryset, many=True)
        return Response(serializer.data)
