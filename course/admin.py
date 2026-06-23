from django.contrib import admin
from course.models import Course, Category, Section,  Lesson, Score, Reply, Comment, ReplayComment, Enrollment

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["title","final_price","is_free", "short_description","status", "degree", "created_date", "published_date"]
    search_fields = ["title", "short_description"]
    list_filter = ('status',"degree", "is_free")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ("name",)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["title"]
    search_fields = ["title"]
    list_filter = ('title',)
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["title", "duration"]
    search_fields = ["title"]
    list_filter = ('duration',)

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["name","email","score", "course"]
    search_fields = ["name", "comment", "course"]
    list_filter = ('email',"score", "course")

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["name"]
    search_fields = ["name", "comment"]
    list_filter = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["author", "course"]
    search_fields = ["author", "comment"]
    list_filter = ('author', "course")

@admin.register(ReplayComment)
class ReplayCommentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["author", "question_comment"]
    search_fields = ["author", "question_comment"]
    list_filter = ('author', "question_comment")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["user", "course"]
    search_fields = ["user", "course"]
    list_filter = ('course',)