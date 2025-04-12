from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from app_cart.models import Order
from ..serializers.order_serializers import OrderSerializer


class OrderView(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def get_list(self, request):

        snippets = Order.objects

        dt_length = int(self.request.query_params.get('length'))
        dt_start = int(self.request.query_params.get('start'))
        dt_draw = self.request.query_params.get('draw')
        dt_search = self.request.query_params.get('search[value]')

        if dt_search:
            snippets = snippets.filter(Q(email__icontains=dt_search) | Q(first_name__icontains=dt_search) | Q(
                last_name__icontains=dt_search) | Q(username__icontains=dt_search))

        records_total = snippets.count()

        serializer = OrderSerializer(snippets.order_by(
            '-id')[dt_start:dt_start+dt_length], many=True)

        return Response({'draw': dt_draw,
                         "recordsTotal": records_total,
                         "recordsFiltered": records_total,
                         'data': serializer.data})
