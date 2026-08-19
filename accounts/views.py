from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from .permissions import IsAdmin


class RegisterView(generics.CreateAPIView):
    """
    POST /api/register/
    only an Admin can hit this, used to create Managers and Users and
    assign their role right away
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdmin]


class UserListView(generics.ListAPIView):
    """
    GET /api/users/
    Admin gets everyone, Manager gets only the people on their team,
    a plain User only ever sees themself here
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "ADMIN":
            return User.objects.all().order_by("id")
        if user.role == "MANAGER":
            return User.objects.filter(manager=user).order_by("id")
        return User.objects.filter(id=user.id)


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PUT /api/me/ - everyone can look at and edit their own profile here"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
