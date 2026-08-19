from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from .permissions import TaskPermission


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, TaskPermission]

    def get_queryset(self):
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
