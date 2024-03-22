from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth.hashers import make_password

from students.models import User


class UserProfileView(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def admin_reset_password(self, request):
        
        status = False
        message = "Failed to update password"

        new_password = request.POST.get('password')
        user_id = request.POST.get('user_id')

        if not new_password or new_password == "":
            message = "Password can't empty or null"

        if not user_id or user_id == "":
            message = "User ID can't empty or null"
        
        if user_id and new_password:
            user = User.objects.get(pk=user_id)
            if user is None:
                message = "User not found"
            else:
                user.password = make_password(new_password)
                user.save()
                message = "Password has been changed: " + new_password
                status = True

        return Response({
                'status':status,
                'message':message,
                'data':0
            })