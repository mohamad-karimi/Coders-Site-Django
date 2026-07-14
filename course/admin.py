from django.contrib import admin
from course.models import Course, Category, Section,  Lesson, Score, Comment, ReplayComment, Enrollment, LessonProgress, CourseProgress, Purchase

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["title","final_price","is_free", "short_description","status", "certification", "created_date", "published_date"]
    search_fields = ["title", "short_description"]
    list_filter = ('status',"certification", "is_free")

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
    list_display = ["user","score", "course"]
    search_fields = ["user", "comment", "course"]
    list_filter = ("score", "course")

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

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["user", "is_completed", "lesson"]
    search_fields = ["user", "lesson"]
    list_filter = ('user', "is_completed")

@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["user", "course", "is_completed", "certificate_received"]
    search_fields = ["user", "course"]
    list_filter = ('user', "is_completed", "certificate_received")

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["user", "course", "amount"]
    search_fields = ["user", "course"]
    list_filter = ('user', "amount")