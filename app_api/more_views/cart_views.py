from unittest import result
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse

from app_cart.models import Order, Package, PackageCourse
from courses.models import Subject
from app_api.more_serializers.cart_serializers import OrderSerializer, PackageSerializer, PackageCourseSerializer

import json


class OrderApiView(APIView):

    def get(self, request, format=None):

        snippets = Order.objects
        ref_id = request.GET.get('ref')
        user_id = request.GET.get('user')

        if ref_id is not None:
            snippets = snippets.filter(ref_id=ref_id)

        if user_id is not None:
            snippets = snippets.filter(user_id=user_id)

        serializer = OrderSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackageApiView(APIView):

    def get_object(self, pk):
        try:
            return Package.objects.get(pk=pk)
        except Package.DoesNotExist:
            raise Http404

    def get(self, request, format=None):

        snippets = Package.objects
        is_deleted = request.GET.get('is_deleted')
        id = request.GET.get('id')

        if is_deleted is not None:
            is_deleted = True if is_deleted=="true" else False
            snippets = snippets.filter(is_deleted = is_deleted)

        if id is not None:
            snippets = snippets.filter(pk=id)

        serializer = PackageSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PackageSerializer(data=request.data)
        pk = request.data.get('id')

        if pk is not None and pk != '':
            package = self.get_object(request.data.get('id'))
            serializer = PackageSerializer(package, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.is_deleted = True
        snippet.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PackageCourseApiView(APIView):

    def get_object(self, pk):
        try:
            return PackageCourse.objects.get(pk=pk)
        except PackageCourse.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        snippets = PackageCourse.objects
        
        package_id = request.GET.get('package_id')

        if package_id:
            snippets = snippets.filter(package_id=package_id)

        serializer = PackageCourseSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        dataArray = request.POST['tasks']  
        serializer = PackageCourseSerializer(data=json.loads(dataArray), many=True)
        if serializer.is_valid():
            print(serializer.data)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PackageSubjectApiView(APIView):

    def post(self, request, format=None):
        packageId = int(request.POST['package'])  
        subjectId = int(request.POST['subject'])
        method = request.POST['method']
        result = 0
        print(subjectId)
        packageObject = Package.objects.get(pk=packageId)
        
        if method == 'add':
            packageObject.subjects.add(subjectId)
            result = 1
        else:
             packageObject.subjects.remove(subjectId)
             result = 1
       
        return Response(result, status=status.HTTP_201_CREATED)