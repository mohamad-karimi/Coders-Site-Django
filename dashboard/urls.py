from django.urls import path
from dashboard.views import dashboard, course_list, course_resume, delete_account

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('course-list/', course_list, name="course_list"),
    path('course-resume/', course_resume, name="course_resume"),
    path("delete-account/", delete_account, name="delete_account")
]