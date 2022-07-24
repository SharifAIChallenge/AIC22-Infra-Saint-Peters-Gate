from rest_framework.permissions import BasePermission

from gateway import settings


class IsBackend(BasePermission):

    def has_permission(self, request, view):
        print("loooog", request.headers.get('Authorization'), len(settings.BACKEND_TOKEN))
        return request.headers.get('Authorization') == settings.BACKEND_TOKEN
