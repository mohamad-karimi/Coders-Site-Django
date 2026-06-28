from django.contrib.syndication.views import Feed
from .models import Course

class CourseFeed(Feed):
    title = "Latest Courses"
    link = "/course/"
    description = "New educational courses"

    def items(self):
        return Course.objects.filter(status=True).order_by("-created_date")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_description

    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_author_name(self, item):
        return item.instructor.name