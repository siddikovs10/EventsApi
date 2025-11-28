from rest_framework import permissions

class IsEventOrganizer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.organizer == request.user

class IsTicketOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsBookingOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsVerifiedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated