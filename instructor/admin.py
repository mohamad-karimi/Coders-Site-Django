from django.contrib import admin
from instructor.models import Instructor, Education, Skill 

# Register your models here.
@admin.register(Instructor)
class PostAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["name","expertise","email", "experience_of_the_year"]
    search_fields = ["name", "expertise"]
    list_filter = ('email',"experience_of_the_year")

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