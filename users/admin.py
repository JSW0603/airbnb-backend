from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = ( #fieldsets is a list of 2-tuples, in which each 2-tuple represents a <fieldset> on the admin form page
        (
            "Profile",
            {
                "fields": (
                    "profile_picture",
                    "username",
                    "first_name",
                    "last_name",
                    "name",
                    "email",
                    "is_host",
                    "gender",
                    "language",
                    "currency",
                ),
            },
        ),
        (
            "Permissions", #Permission 관련 필드들을 묶어서 보여주기 위해서 fieldsets를 사용
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",) #해당 fieldset를 접을 수 있도록 설정
            },
        ),
        (
            "Important dates", 
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
                "classes": ("collapse",)
            },
        ),
    )
    list_display = ("username", "email", "name", "is_host")