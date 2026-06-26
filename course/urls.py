from django.urls import path, re_path
from course.views import course_list, course_categories, course_detail, my_courses

app_name = "course"
urlpatterns = [
    path('list/', course_list, name="course_list"),
    path('categories/', course_categories, name="course_categories"),
    re_path(r'^course/(?P<slug>[-\w\u0600-\u06FF]+)/$', course_detail, name='course_detail'),
    path('category/<str:ca_name>/', course_list, name='course_category'),
    path('tag/<str:ta_name>/', course_list, name='course_tag'),
    path('skill/<str:sk_name>/', course_list, name='course_skill_level'),
    path('my-courses/', my_courses, name='student_courses')
]