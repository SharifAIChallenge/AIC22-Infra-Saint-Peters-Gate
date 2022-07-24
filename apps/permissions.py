from rest_framework.permissions import BasePermission
import os

from gateway import settings


class IsBackend(BasePermission):

    def has_permission(self, request, view):
        print("hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        raise Exception("loooog", request.headers.get('Authorization'), len(os.environ["BACKEND_TOKEN"]))
        return request.headers.get('Authorization') == settings.BACKEND_TOKEN
