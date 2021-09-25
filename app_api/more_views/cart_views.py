from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from app_cart.models import Order
from app_api.more_serializers.cart_serializers import OrderSerializer

from django.utils.timezone import localtime, now


class OrderApiView(APIView):

    def get(self, request, format=None):

        snippets = Order.objects
        ref_id = request.GET.get('ref')

        if ref_id is not None:
            snippets = snippets.filter(ref_id = ref_id)

        serializer = OrderSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
