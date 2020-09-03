
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Count

from ..serializers import UserSerializer

from students.models import User
from django.conf import settings


class UserDetailView(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        snippets = User.objects.all()
        serializer = UserSerializer(snippets.order_by('-id'), many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None,):
        snippet = self.get_object(pk)
        snippet.is_deleted = True
        snippet.save()

        return Response(status=status.HTTP_204_NO_CONTENT)