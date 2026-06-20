from django.urls import path
from instructor.views import IN_list, IN_single

app_name = "instructor"
urlpatterns = [
    path('list/', IN_list, name="instructor_list"),
    path('single/', IN_single, name="instructor_single"),
]