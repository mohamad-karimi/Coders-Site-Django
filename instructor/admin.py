from django.contrib import admin
from instructor.models import Instructor, Education, Skill 

# Register your models here.
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"

    list_display = ["username", "expertise", "email", "experience_of_the_year",]

    search_fields = ["user__username", "expertise", "user__email",]

    list_filter = ("experience_of_the_year",)

    def username(self, obj):
        return obj.user.username

    username.short_description = "Username"

    def email(self, obj):
        return obj.user.email

    email.short_description = "Email"

@admin.register(Education)
class PostAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["university","field_of_study",]
    search_fields = ["university", "field_of_study"]
    list_filter = ('university',"field_of_study")

@admin.register(Skill)
class PostAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["name","amount",]
    search_fields = ["name"]
    list_filter = ('amount',)