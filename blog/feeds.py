from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class BlogFeed(Feed):
    title = "Latest Blog Posts"
    link = "/blog/"
    description = "New articles from our blog"

    def items(self):
        return Post.objects.filter(status=True).order_by("-created_date")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.info

    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_author_name(self, item):
        return item.author.username