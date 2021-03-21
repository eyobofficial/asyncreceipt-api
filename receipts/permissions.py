from rest_framework import permissions


class IsReceiptOwner(permissions.BasePermission):
    """Check if a user is the creator of the receipt."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
