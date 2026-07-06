from django.urls import path, re_path
from blog.views import blog_grid, blog_detail, like_post, search

app_name = "blog"

urlpatterns = [
    path('', blog_grid, name="blog_grid"),
    path('search/', search, name='search'),
    re_path(r'^course/(?P<slug>[-\w\u0600-\u06FF]+)/$', blog_detail, name='blog_detail'),
    path('category/<str:ca_name>/', blog_grid, name='blog_category'),
    path('author/<str:au_name>/', blog_grid, name='blog_author'),
    path('tag/<str:ta_name>/', blog_grid, name='blog_tag'),
    path('like/<int:pk>/', like_post, name='like_post'),
]