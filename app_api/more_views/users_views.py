from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import Http404
from django.db.models import Count
from django.conf import settings
from datetime import datetime
from cryptography.fernet import Fernet
from rest_framework.pagination import PageNumberPagination
import json

from app_api.serializers import UserSerializer
from app_api.permissions import IsTeacherUser
from app_api.more_serializers.student_serializers import SSTCardSerializer

from students.models import User, SSTCard


class UserPaginator(PageNumberPagination):
    page_size = 10  # Number of objects to return in one page

    def generate_response(self, query_set, serializer_obj, request):
        try:
            page_data = self.paginate_queryset(query_set, request)
        except:
            return Response({"error": "No results found for the requested page"}, status=status.HTTP_400_BAD_REQUEST)

        print(query_set.count())

        serialized_page = serializer_obj(page_data, many=True)

        res = Response({'count': page_data.count,
                       'results': serialized_page.data})

        print(res)
        return res

        return self.get_paginated_response(serialized_page.data)


class UserDetailView(APIView):
    # permission_classes = [IsTeacherUser | IsAdminUser]
    page_size = 3

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id=None, format=None):

        snippets = User.objects
        paginator = UserPaginator()

        if id is not None:
            snippets = snippets.filter(pk=id)

        is_student = self.request.query_params.get('is_student', None)

        if is_student is not None:
            snippets = snippets.filter(is_student=is_student)

        dt_length = int(self.request.query_params.get('length'))
        dt_start = int(self.request.query_params.get('start'))
        dt_draw = self.request.query_params.get('draw')

        records_total = snippets.count()

        serializer = UserSerializer(snippets.order_by('-id')[dt_start:dt_start+dt_length], many=True)

        #return Response(serializer.data)

        return Response({'draw': dt_draw,
                         "recordsTotal": records_total,
                         "recordsFiltered": records_total,
                         'data': serializer.data})

        response = paginator.generate_response(
            snippets.order_by('-id'), UserSerializer, request)

        return response

    def put(self, request, id, format=None):

        snippet = self.get_object(id)
        serializer = UserSerializer(snippet, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None,):
        snippet = self.get_object(pk)
        is_active = request.data['is_active']
        snippet.is_active = is_active
        snippet.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SSTCardApiView(APIView):

    def get_object(self, pk):
        try:
            return SSTCard.objects.get(pk=pk)
        except SSTCard.DoesNotExist:
            raise Http404

    def get(self, request, format=None):

        snippets = SSTCard.objects.all()

        card_number = self.request.query_params.get('card_number', None)

        if card_number is not None:
            snippets = snippets.filter(card_id=card_number)

        serializer = SSTCardSerializer(snippets.order_by('-id'), many=True)

        return Response(serializer.data)


@api_view(['POST'])
def EmailExist(request):
    result = True

    if request.method == 'POST':
        email = request.POST['email']
        count = User.objects.filter(email=email).count()
        if count > 0:
            result = False

    return Response(result)
