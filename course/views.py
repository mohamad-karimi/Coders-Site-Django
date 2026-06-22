from django.shortcuts import render
from course.models import Course
# Create your views here.
def course_list(request):
    course = Course.objects.filter(status=True)
    context = {"course":course}
    
    return render(request, 'course/course-list.html', context)

def course_categories(request):
    return render(request, 'course/course-categories.html')

def course_detail(request):
    return render(request, 'course/course-detail.html')