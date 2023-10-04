from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import Http404
from django.db.models import Count, Q
from django.conf import settings
from datetime import datetime
from cryptography.fernet import Fernet
from rest_framework.pagination import PageNumberPagination

import json

from app_api.serializers import UserSerializer
from app_api.permissions import IsTeacherUser
from app_api.more_serializers.student_serializers import SSTCardSerializer

from students.models import User, SSTCard


class UserDetailView(APIView):
    # permission_classes = [IsTeacherUser | IsAdminUser]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):

        snippets = User.objects

        if pk is not None:
            snippets = snippets.filter(pk=pk)
            serializer = UserSerializer(snippets, many=True)
            return Response(serializer.data)

        is_student = self.request.query_params.get('is_student', None)

        if is_student is not None:
            snippets = snippets.filter(is_student=is_student)

        is_active = self.request.query_params.get('is_active')
        snippets = snippets.filter(is_active=is_active)

        dt_length = int(self.request.query_params.get('length'))
        dt_start = int(self.request.query_params.get('start'))
        dt_draw = self.request.query_params.get('draw')
        dt_search = self.request.query_params.get('search[value]')


        if dt_search:
            snippets = snippets.filter(Q(email__icontains=dt_search) | Q(first_name__icontains=dt_search) | Q(
                last_name__icontains=dt_search) | Q(username__icontains=dt_search))

        records_total = snippets.count()

        serializer = UserSerializer(snippets.order_by(
            '-id')[dt_start:dt_start+dt_length], many=True)

        # return Response(serializer.data)

        return Response({'draw': dt_draw,
                         "recordsTotal": records_total,
                         "recordsFiltered": records_total,
                         'data': serializer.data})

    def put(self, request, pk, format=None):

        snippet = self.get_object(pk)
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

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        #is_active = request.data['is_active']
        snippet.is_active = 0
        snippet.save()

        return Response(status=status.HTTP_201_CREATED)


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
