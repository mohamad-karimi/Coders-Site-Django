from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from course.models import Course, CourseProgress

# Create your views here.
def dashboard(request):
    courses_count = Course.objects.all().count()

    certificates_count = CourseProgress.objects.filter(
        user=request.user,
        certificate_received=True
    ).count()

    context = {
        "courses_count": courses_count,
        "certificates_count": certificates_count,
    }

    return render(request, 'dashboard/student-dashboard.html', context)

def course_list(request):
    return render(request, 'dashboard/student-course-list.html')

def course_resume(request):
    return render(request, 'dashboard/student-course-resume.html')

@login_required
def delete_account(request):
    if request.method == "GET":
        request.user.delete()
        return redirect("/")

    return redirect("dashboard:dashboard")