from django.contrib import admin
from website.models import contact
# Register your models here.
@admin.register(contact)
class contactAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["name", "email"]
    search_fields = ["name", "message"]
    list_filter = ('email',)