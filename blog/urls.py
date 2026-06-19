from django.urls import path
from blog.views import blog_grid, blog_detail
urlpatterns = [
    path('', blog_grid, name="blog_grid"),
    path('detail/', blog_detail, name="blog_detail"),
]