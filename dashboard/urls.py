from django.urls import path
from dashboard.views import dashboard, bookmark, course_list, course_resume

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('bookmark/', bookmark, name="bookmark"),
    path('course-list/', course_list, name="course_list"),
    path('course-resume/', course_resume, name="course_resume"),
    
]