from django.shortcuts import render
from course.models import Course, CourseProgress
from django.db.models import Q

# Create your views here.
def dashboard(request):
    courses = Course.objects.filter(
        status=True,
        enrollment__user=request.user
    ).distinct()

    s = request.GET.get("s")
    if s:
        courses = courses.filter(
            Q(title__icontains=s) |
            Q(overview__icontains=s)
        )

    courses_count = courses.count()

    certificates_count = CourseProgress.objects.filter(
        user=request.user,
        certificate_received=True
    ).count()

    context = {
        "courses": courses,
        "courses_count": courses_count,
        "certificates_count": certificates_count,
    }

    return render(request, 'dashboard/student-dashboard.html', context)

def course_list(request):
    courses = Course.objects.filter(
        status=True,
        enrollment__user=request.user
    ).distinct()
    
    s = request.GET.get("s")
    if s:
        courses = courses.filter(
            Q(title__icontains=s) |
            Q(overview__icontains=s)
        )


    context = {
        "courses" : courses,
    }
    return render(request, 'dashboard/student-course-list.html', context)

def course_resume(request):
    return render(request, 'dashboard/student-course-resume.html')