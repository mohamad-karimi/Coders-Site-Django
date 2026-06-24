from django.contrib import admin
from website.models import Contact, Question, Answer, MentorUser
# Register your models here.
@admin.register(Contact)
class contactAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["name", "email"]
    search_fields = ["name", "message"]
    list_filter = ('email',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["name"]
    search_fields = ["name", "text"]
    list_filter = ('name',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["question"]
    search_fields = ["question", "text"]
    list_filter = ('question',)

@admin.register(MentorUser)
class MentorUserAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["name", "email", "expertise"]
    search_fields = ["name", "expertise"]
    list_filter = ('email', 'expertise')