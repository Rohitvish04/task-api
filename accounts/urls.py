from django.urls import path
from .views import RegisterView, UserListView, MeView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("users/", UserListView.as_view()),
    path("me/", MeView.as_view()),
]
