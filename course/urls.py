from django.urls import path
from course.views import course_list, course_categories, course_detail

urlpatterns = [
    path('list/', course_list, name="course_list"),
    path('categories/', course_categories, name="course_categories"),
    path('detail/', course_detail, name="course_detail"),
]