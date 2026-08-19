from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(title="RBAC Task API", default_version="v1"),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),

    path("api/", include("accounts.urls")),
    path("api/", include("tasks.urls")),

    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
]
