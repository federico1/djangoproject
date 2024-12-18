from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app_cart.models import Order

from app_api.more_serializers.cart_serializers import OrderSerializer



class OrderApiView(APIView):

    def get(self, request, format=None):

        snippets = Order.objects
        ref_id = request.GET.get('ref')
        user_id = request.GET.get('user')

        if ref_id is not None:
            snippets = snippets.filter(ref_id=ref_id)

        if user_id is not None:
            snippets = snippets.filter(user_id=user_id)

        serializer = OrderSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user_id = serializer.validated_data.get('user').id
            if request.user.id != user_id:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

