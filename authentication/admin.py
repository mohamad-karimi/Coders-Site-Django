from django.contrib import admin
from authentication.models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    empty_value_display = "-empty-"
    list_display = ["username", "email", "role"]
    search_fields = ["username"]
    list_filter = ('username', "email", "role")

    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {
            "fields": ("avatar", "role")
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Info", {
            "fields": ("email", "avatar", "role")
        }),
    )