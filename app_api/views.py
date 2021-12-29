from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import Http404
from django.utils.timezone import localtime, now
from django.conf import settings

from app_chat.models import VideoRoom, VideoParticipant, Notification, ParticipantLog, VideoCourses

from .serializers import CourseSerializer, UserSerializer, \
    VideoRoomSerializer, VideoParticipantSerializer, NotificationSerializer, ParticipantLogSerializer, \
    VideoCoursesSerializer

from students.models import User
from app_api.helpers import save_base64


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
            snippets = VideoRoom.objects.filter(
                owner=request.user, is_deleted=False)
        else:
            ps = VideoParticipant.objects.filter(
                member=request.user).values_list('room_id', flat=True)
            snippets = VideoRoom.objects.filter(id__in=ps, is_deleted=False)

        serializer = VideoRoomSerializer(snippets.order_by('-id'), many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VideoRoomSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None,):
        snippet = self.get_object(pk)
        snippet.is_deleted = True
        snippet.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoCoursesView(APIView):

    def get_object(self, pk):
        try:
            return VideoCourses.objects.get(pk=pk)
        except VideoCourses.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        c_id = request.query_params.get('room')

        snippets = VideoCourses.objects.filter(room_id=c_id)
        serializer = VideoCoursesSerializer(snippets, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VideoCoursesSerializer(data=request.data, many=True)

        r = request.query_params.get('r')

        if r:
            VideoCourses.objects.filter(room_id=int(r)).delete()

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


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

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = VideoParticipantSerializer(
            snippet, data={'member': snippet.member.id, 'is_approved': True})
        if serializer.is_valid():
            rs = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class ParticipantLogDetailView(APIView):

    def get_object(self, pk):
        try:
            return ParticipantLog.objects.get(pk=pk)
        except ParticipantLog.DoesNotExist:
            raise Http404

    def get(self, request, format=None):

        room = request.query_params.get('room')

        snippets = ParticipantLog.objects.filter(room_id=room).order_by('-id')

        serializer = ParticipantLogSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ParticipantLogSerializer(data=request.data)

        print(serializer)
        if serializer.is_valid():
            serializer.save(participant=request.user)

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def SaveBase64ImageView(request):

    result = ""
    message = ""

    if request.method == 'POST':
        image_name = "attendee"

        if request.user:
            image_name = image_name + "_" + str(request.user.id)

        image_name = image_name + "_" + \
            localtime(now()).strftime("%y%m%d%H%M%S")

        if request.data['course']:
            image_name = image_name + "_" + request.data['course']

        image_name = image_name + ".png"

        result = save_base64(image_name, request.data['image_data'])

    return Response({"message": message, "result": result})
