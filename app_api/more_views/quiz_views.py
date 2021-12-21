from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json

from students.models import Quiz
from app_api.more_serializers.quiz_serializers import QuizCoreSerializer


class QuizApiView(APIView):

    def get(self, request, format=None):
        snippets = Quiz.objects

        owner_id = request.query_params.get('owner')

        if owner_id:
            snippets = snippets.filter(owner_id=owner_id)
        
        snippets = snippets.order_by('-id')
        
        serializer = QuizCoreSerializer(snippets, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
      
        serializer = QuizCoreSerializer(data=request.data)
        

        if serializer.is_valid():
            
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
