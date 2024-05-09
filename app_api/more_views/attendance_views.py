from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from courses.models import Attendance
from app_api.more_serializers.course_serializers import AttendanceSerializer

from django.utils.timezone import localtime, now

class AttendanceApiView(APIView):

    def get(self, request, format=None):

        snippets = Attendance.objects.all()

        course_id = request.query_params.get('course')
        today = request.query_params.get('today')
        student_id = request.query_params.get('student')

        if course_id:
            snippets = snippets.filter(course_id=course_id)

        if student_id:
            snippets = snippets.filter(student_id=student_id)
        
        if today:
            snippets = snippets.filter(
                created__startswith=localtime(now()).date())

        serializer = AttendanceSerializer(snippets, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AttendanceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ApproveAttendance(request):

    result = 0
    message = ""

    if request.method == 'POST':
        data_object = Attendance.objects.get(pk=request.data['id'])
        data_object.is_approved = request.data['is_approved']
        data_object.save()

        result = 1

    return Response({"message": message, "result": result})
