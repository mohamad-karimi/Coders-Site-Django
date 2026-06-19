from django.shortcuts import render

# Create your views here.
def blog_grid(request):
    return render(request, 'blog/blog-grid.html')

def blog_detail(request):
    return render(request, 'blog/blog-detail.html')