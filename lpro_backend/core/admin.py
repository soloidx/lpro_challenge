from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User


class CustomUserAdmin(UserAdmin):
    list_display = tuple([x for x in UserAdmin.list_display if x != "username"])
    search_fields = tuple([x for x in UserAdmin.search_fields if x != "username"])
    ordering = ("email",)
    fieldsets = (
        (
            None,
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "Personal info",
            {
                "fields": ("first_name", "last_name"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            "Account",
            {"fields": ("balance",)},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
