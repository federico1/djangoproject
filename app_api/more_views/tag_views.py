from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from students.models import Tag
from app_api.more_serializers.tag_serializers import TagSerializer


class TagApiView(APIView):

    def get(self, request, format=None):
        snippets = Tag.objects

        serializer = TagSerializer(snippets, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TagSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

