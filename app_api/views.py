from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from app_chat.models import Conversation, Message, ConversationMember, \
    VideoRoom, VideoParticipant, Notification

from .serializers import ConversationSerializer, CourseSerializer, \
    UserSerializer, ConversationMemberSerializer, MessageSerializer, \
    VideoRoomSerializer, VideoParticipantSerializer, NotificationSerializer

from students.models import User

from django.conf import settings


class ConversationDetailView(APIView):

    def get_object(self, pk):
        try:
            return Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        snippets = Conversation.objects.filter(owner=request.user)

        if request.user.is_student == True:
            c_list = \
                request.user.conversation_member.values_list('conversation_id'
                    , flat=True)
            snippets = Conversation.objects.filter(id__in=c_list)

        serializer = ConversationSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self,
        request,
        pk,
        format=None,
        ):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConversationMembersList(APIView):

    def get_object(self, pk):
        try:
            return ConversationMember.objects.get(pk=pk)
        except ConversationMember.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        c_id = request.query_params.get('conversation')
        snippets = \
            ConversationMember.objects.filter(conversation_id=c_id)
        serializer = ConversationMemberSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ConversationMemberSerializer(data=request.data)
        if serializer.is_valid():
            a_count = \
                ConversationMember.objects.filter(conversation_id=int(request.data['conversation'
                    ]), member_id=int(request.data['member'])).count()

            if a_count <= 0:
                serializer.save()

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self,
        request,
        pk,
        format=None,
        ):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageList(APIView):

    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        c_id = request.query_params.get('conversation')
        type = request.query_params.get('type')

        snippets = Message.objects.filter(conversation_id=c_id)

        if type is not None or type == 'last10':
            snippets = \
                Message.objects.filter(conversation_id=c_id).order_by('-id'
                    )[:10][::-1]

        serializer = MessageSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self,
        request,
        pk,
        format=None,
        ):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherCoursesDetailView(APIView):

    def get(self, request, format=None):
        snippets = request.user.courses_created
        serializer = CourseSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():

            # serializer.save()

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class TeacherStudentsList(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        users_id = \
            list(request.user.courses_created.values_list('students',
                 flat=True))
        queryset = self.get_queryset().filter(id__in=users_id)
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data)


class VideoRoomDetailView(APIView):

    def get_object(self, pk):
        try:
            return VideoRoom.objects.get(pk=pk)
        except VideoRoom.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        snippets = None

        if request.user.is_teacher == True:
            snippets = VideoRoom.objects.filter(owner=request.user, is_deleted = False)
        else:
            ps = VideoParticipant.objects.filter(member=request.user).values_list('room_id', flat=True)
            snippets = VideoRoom.objects.filter(id__in=ps, is_deleted = False)
        
        serializer = VideoRoomSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VideoRoomSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk,format=None,):
        snippet = self.get_object(pk)
        snippet.is_deleted = True
        snippet.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class VideoParticipantView(APIView):

    def get_object(self, pk):
        try:
            return VideoParticipant.objects.get(pk=pk)
        except VideoParticipant.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        c_id = request.query_params.get('room')
        snippets = \
            VideoParticipant.objects.filter(room_id=c_id)
        serializer = VideoParticipantSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VideoParticipantSerializer(data=request.data)
        if serializer.is_valid():
            a_count = \
                VideoParticipant.objects.filter(room_id=int(request.data['room'
                    ]), member_id=int(request.data['member'])).count()

            if a_count <= 0:
                serializer.save()

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self,
        request,
        pk,
        format=None,
        ):
        print(pk)
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationDetailView(APIView):

    def get_object(self, pk):
        try:
            return Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            raise Http404

    def get(self, request, format=None):

        n_status = request.query_params.get('status')

        snippets = Notification.objects.filter(receiver=request.user)

        if n_status is not None:
            snippets = \
                snippets.filter(status=n_status).order_by('-id')

        serializer = NotificationSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)