
# from django.shortcuts import get_object_or_404
# from rest_framework import generics
# from rest_framework import viewsets
# from rest_framework.authentication import BasicAuthentication
# from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import Http404
from django.db.models import Count

from app_api.serializers import UserSerializer
from app_api.permissions import IsTeacherUser
from app_api.more_serializers.student_serializers import SSTCardSerializer

from students.models import User, SSTCard
from django.conf import settings


class UserDetailView(APIView):
    # permission_classes = [IsTeacherUser | IsAdminUser]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        snippets = User.objects.all()

        is_student = self.request.query_params.get('is_student', None)

        if is_student is not None:
            snippets = snippets.filter(is_student=is_student)

        serializer = UserSerializer(snippets.order_by('-id'), many=True)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserSerializer(snippet, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
       
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None,):
        snippet = self.get_object(pk)
        is_active =  request.data['is_active']
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


