from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from courses.models import StudentCertificate
from app_api_v2.serializers import student_serializers



class StudentCertificateView(viewsets.ViewSet):


    @action(detail=False, methods=['get'])
    def verify(self, request):

        queryset = StudentCertificate.objects
        ref_number = request.query_params.get('ref_number')
        
        if ref_number:
            queryset = queryset.filter(ref_number=ref_number)
        else:
            return Response([],
                            status=status.HTTP_400_BAD_REQUEST)
        
        if queryset.count() <=0:
            return Response({
                'status':False,
                'message':'We are not able to found any record.',
                'data':{}
            })

        queryset = queryset.first()

        serializer = student_serializers.CertificateVerficationSerializer(queryset, many=False)

        return Response({
                'status':True,
                'message':'success',
                'data':serializer.data
            })


