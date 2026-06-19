from django.urls import path
from course.views import course_list, course_grid, course_detail

urlpatterns = [
    path('list/', course_list, name="course_list"),
    path('grid/', course_grid, name="course_grid"),
    path('detail/', course_detail, name="course_detail"),
]