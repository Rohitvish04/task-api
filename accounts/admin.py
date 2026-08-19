from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Role & Team", {"fields": ("role", "manager")}),
    )
    list_display = ("username", "email", "role", "manager", "is_staff")
    list_filter = ("role",)


admin.site.register(User, CustomUserAdmin)
