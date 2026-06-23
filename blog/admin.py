from django.contrib import admin
from blog.models import Post, Category
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["title", "author", "status", "views", "like", "published_date"]
    search_fields = ["title", "content"]
    list_filter = ('status', "author")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ('name',)