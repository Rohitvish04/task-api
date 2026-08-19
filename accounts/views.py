from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from .permissions import IsAdmin


class RegisterView(generics.CreateAPIView):
    """
    only an Admin can hit this, used to create Managers and Users and
    assign their role right away
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_summary="Create a new account (Admin only)",
        operation_description=(
            "Creates a Manager or a User account and assigns its role right away.\n\n"
            "- `role=USER` requires a `manager` id in the body.\n"
            "- `role=MANAGER` or `role=ADMIN` must NOT include a `manager` id.\n\n"
            "Only an Admin token can call this — anyone else gets a 403."
        ),
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserListView(generics.ListAPIView):
    """
    Admin gets everyone, Manager gets only the people on their team,
    a plain User only ever sees themself here
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List users (scoped to your role)",
        operation_description=(
            "Returns a different list depending on who's logged in:\n\n"
            "- **Admin** → every user in the system\n"
            "- **Manager** → only the users whose `manager` field points at them\n"
            "- **User** → only themself"
        ),
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.role == "ADMIN":
            return User.objects.all().order_by("id")
        if user.role == "MANAGER":
            return User.objects.filter(manager=user).order_by("id")
        return User.objects.filter(id=user.id)
