from django.shortcuts import render
from blog.models import Post

# Create your views here.
def blog_grid(request):
    posts = Post.objects.filter(status = True)

    context={"posts":posts}
    return render(request, 'blog/blog-grid.html', context)

def blog_detail(request, slug):
    post = Post.objects.get(slug=slug, status=True)

    context = {
        "post": post
    }
    return render(request, 'blog/blog-detail.html', context)