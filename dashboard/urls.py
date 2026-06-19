from django.urls import path
from dashboard.views import dashboard, bookmark, course_list, course_resume

urlpatterns = [
    path('', dashboard, name="st_dashboard"),
    path('bookmark/', bookmark, name="st_bookmark"),
    path('course-list/', course_list, name="st_course_list"),
    path('course-resume/', course_resume, name="st_course_resume"),
    
]