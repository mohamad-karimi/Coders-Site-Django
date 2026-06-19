from django.shortcuts import render

# Create your views here.
def course_list(request):
    return render(request, 'course/course-list.html')

def course_grid(request):
    return render(request, 'course/course-grid.html')

def course_detail(request):
    return render(request, 'course/course-detail.html')