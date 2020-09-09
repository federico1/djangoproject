
from rest_framework import permissions


class IsTeacherUser(permissions.BasePermission):
    message = 'User is not allowed.'

    def has_permission(self, request, view):
        print(request.user.is_teacher)
        return request.user.is_teacher