from rest_framework.permissions import  BasePermission
from django.contrib.auth.models import User

class UserPermission(BasePermission):
    message = 'no autorizado'
    model = User
    def has_permission(self, request, view):
        name = view.model.__name__.lower()
        app = view.model._meta.app_label
        perm = view.permission_required
        if request.user.is_superuser:
            return True
        else:
            return request.user.has_perm(perm)
            
    def has_object_permission(self, request, view, object):
        # Your permission logic per object
        return True