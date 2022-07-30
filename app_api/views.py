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

from app_chat.models import  Notification

from .serializers import CourseSerializer, UserSerializer, NotificationSerializer
    

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
