from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from .permissions import TaskPermission


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, TaskPermission]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Task.objects.none()

        user = self.request.user
        if user.role == "ADMIN":
            return Task.objects.all()
        if user.role == "MANAGER":
            # union of their own tasks + their team's tasks - without the
            # second filter a manager wouldn't see tasks they made themselves
            return Task.objects.filter(owner__manager=user) | Task.objects.filter(owner=user)
        return Task.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        operation_summary="List tasks (scoped to your role)",
        operation_description=(
            "Admin sees every task, Manager sees their own tasks plus their team's, "
            "a plain User sees only their own."
        ),
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a task",
        operation_description="Owner is set automatically to whoever is logged in — you can't create a task for someone else.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get a single task",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a task (full)",
        operation_description="Allowed for the task's owner, the owner's manager, or an Admin. Send every field.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a task (partial)",
        operation_description="Same permission rules as full update, but only send the field(s) you're changing.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a task (Admin only)",
        operation_description="Blocked for everyone except Admin, even if you own the task yourself.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
