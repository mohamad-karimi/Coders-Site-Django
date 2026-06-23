from django.urls import path
from blog.views import blog_grid, blog_detail
from django.urls import re_path

app_name = "blog"

urlpatterns = [
    path('', blog_grid, name="blog_grid"),
    re_path(r'^course/(?P<slug>[-\w\u0600-\u06FF]+)/$', blog_detail, name='blog_detail'),
    path('category/<str:ca_name>/', blog_grid, name='blog_category'),
    path('author/<str:au_name>/', blog_grid, name='blog_author'),
]