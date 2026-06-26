from django.urls import path, re_path
from instructor.views import IN_list, IN_single, instructor_search

app_name = "instructor"
urlpatterns = [
    path('list/', IN_list, name="instructor_list"),
    path("search/", instructor_search, name="instructor_search"),
    path('<slug:slug>/', IN_single, name="instructor_single"),
    re_path(r'^course/(?P<slug>[-\w\u0600-\u06FF]+)/$', IN_single, name='instructor_single'),
]