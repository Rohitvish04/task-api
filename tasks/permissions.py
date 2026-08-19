from rest_framework.permissions import BasePermission


class TaskPermission(BasePermission):
    """
    list/create is open to any logged in role (queryset filtering handles
    who actually sees what). delete is admin only. update is allowed for
    the task owner or that owner's manager.
    """

    def has_permission(self, request, view):
        if request.method == "DELETE":
            return request.user.role == "ADMIN"
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == "ADMIN":
            return True

        if user.role == "MANAGER":
            return obj.owner == user or obj.owner.manager_id == user.id

        return obj.owner == user
