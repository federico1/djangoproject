from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.http import Http404
from django.db.models import Count

from app_chat.models import ExternalVideoRoom
from app_api.more_serializers.chat_serializers import ExternalVideoRoomSerializer

from students.models import User
from django.conf import settings

from django.utils.timezone import localtime, now


class ExternalVideoRoomDetailView(APIView):

    def get_object(self, pk):
        try:
            return ExternalVideoRoom.objects.get(pk=pk)
        except ExternalVideoRoom.DoesNotExist:
            raise Http404

    def get(self, request, format=None):

        course_id = request.query_params.get('course')
        today = request.query_params.get('today')
        is_delete = request.query_params.get('delete')

        snippets = ExternalVideoRoom.objects.filter(course_id=course_id)
        
        if today:
            snippets = snippets.filter(created__startswith=localtime(now()).date())
        
        if is_delete:
            is_delete =  True if is_delete == 'true' else False
            
            snippets = snippets.filter(is_deleted=is_delete)

        serializer = ExternalVideoRoomSerializer(snippets, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ExternalVideoRoomSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.is_deleted = True
        snippet.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
