from django.contrib import admin
from authentication.models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    empty_value_display = "-empty-"
    list_display = ["username", "email"]
    search_fields = ["username"]
    list_filter = ('username', "email")

    fieldsets = UserAdmin.fieldsets + (
        ("اطلاعات اضافی", {
            "fields": ("avatar",)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("اطلاعات اضافی", {
            "fields": ("avatar",)
        }),
    )