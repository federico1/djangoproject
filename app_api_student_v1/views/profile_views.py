from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import logout

class ProfileView(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def switch_to_business_account(self, request):
        
        request.user.is_business = True
        request.user.is_student = False
        request.user.save()
        logout(request)

        return Response({
                'status':True,
                'message':'success',
                'data':0
            })
