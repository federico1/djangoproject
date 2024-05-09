
from rest_framework import permissions


class IsTeacherUser(permissions.BasePermission):
    message = 'User is not allowed.'

    def has_permission(self, request, view):
        return request.user.is_teacher