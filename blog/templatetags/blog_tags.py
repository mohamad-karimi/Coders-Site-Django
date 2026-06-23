from django import template
from blog.models import Post
from django.utils import timezone

register = template.Library()

@register.inclusion_tag('blog/latest_posts.html')
def latest_posts(count=3):
    posts = Post.objects.filter(status = True,  published_date__lte = timezone.now()).order_by("-published_date")[:count]
    return {"posts" : posts}