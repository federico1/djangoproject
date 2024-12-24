from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from app_cart.models import Package
from django.http import Http404
from rest_framework.permissions import IsAdminUser
from ..serializers import cart_serializers


class PackageView(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Package.objects.get(pk=pk)
        except Package.DoesNotExist:
            raise Http404

    def list(self, request):
        is_deleted = request.query_params.get('is_deleted')

        snippets = Package.objects

        if is_deleted is not None:
            snippets = snippets.filter(
                is_deleted=False if is_deleted == 'false' else True)

        serializer = cart_serializers.PackageSerializer(
            snippets, many=True)

        return Response(serializer.data)

    # def create(self, request):
    #     data = request.data

    #     course = Package.objects.get(pk=request.data['package_id'])

    #     data['created_by'] = self.request.user.id

    #     if course.is_free == True:
    #         data['price'] = 0
    #     else:
    #         data['price'] = course.discounted_price if course.discounted_price > 0 else course.price

    #     serializer = cart_serializers.Package(data=data)

    #     if request.user.is_authenticated and request.user.is_student == True and serializer.is_valid():

    #         if course.is_free == False:
    #             return Response(serializer.data, status=status.HTTP_502_BAD_GATEWAY)

    #         if not Enrollments.objects.filter(course=request.data['course'], user=self.request.user).exists():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(serializer.data, status=status.HTTP_226_IM_USED)

    #     serializer.is_valid()

    #     return Response(serializer.errors, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    # @action(detail=True, methods=['post'])
    # def set_completed(self, request, pk=None):
    #     snippet = self.get_object(pk)
    #     snippet.is_completed = request.data['status']
    #     snippet.completed_date = datetime.now()
    #     snippet.save()

    #     serializer = course_serializers.EnrollmentSerializer(snippet)

    #     return Response(serializer.data)
