from rest_framework.permissions import BasePermission

class IsMesero(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.mesero_access')

class IsCocina(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.cocina_access')

class IsCaja(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.caja_access')

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.admin_access')