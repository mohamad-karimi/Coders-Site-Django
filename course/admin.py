from django.contrib import admin
from course.models import Course, Category, Section,  Lesson

# Register your models here.
@admin.register(Course)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["title","final_price","is_free", "short_description","status", "degree", "created_date", "published_date"]
    search_fields = ["title", "short_description"]
    list_filter = ('status',"degree", "is_free")

@admin.register(Category)
class PostAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ("name",)

@admin.register(Section)
class PostAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["title"]
    search_fields = ["title"]
    list_filter = ('title',)
@admin.register(Lesson)
class PostAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["title", "duration"]
    search_fields = ["title"]
    list_filter = ('duration',)