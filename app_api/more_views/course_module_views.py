from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from courses.models import Module

class UpdateQuizApiView(APIView):

    def get_object(self, pk):
        try:
            return Module.objects.get(pk=pk)
        except Module.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        pk = request.POST['id']
        snippet = self.get_object(pk)
        snippet.quiz_id = request.POST['quiz_id']
        snippet.save()
        result = 1
        return Response(result)
