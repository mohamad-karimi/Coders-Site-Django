from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/student-dashboard.html')

def bookmark(request):
    return render(request, 'dashboard/student-bookmark.html')

def course_list(request):
    return render(request, 'dashboard/student-course-list.html')

def course_resume(request):
    return render(request, 'dashboard/student-course-resume.html')

