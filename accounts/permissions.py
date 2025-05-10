from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    """
    Hanya mengizinkan pemilik objek untuk retrieve, update, atau delete.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user