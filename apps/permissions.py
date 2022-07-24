from rest_framework.permissions import BasePermission
import os

from gateway import settings


class IsBackend(BasePermission):

    def has_permission(self, request, view):
        return request.headers.get('Authorization') == settings.BACKEND_TOKEN
