
from rest_framework.views import APIView
from rest_framework.response import Response

from app_api.more_serializers.student_serializers import StudentHistorySerializer
from students.models import User


class StudentsHistoryApiView(APIView):

    def get(self, request, format=None):

        course_id = request.query_params.get('course')

        snippets = User.objects.filter(is_student=True)

        if course_id is not None:
            snippets = snippets.filter(course_enrolled__course=course_id)

        serializer = StudentHistorySerializer(snippets.order_by('-id'), many=True)

        return Response(serializer.data)

