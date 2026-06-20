from django.shortcuts import render

# Create your views here.
def course_list(request):
    return render(request, 'course/course-list.html')

def course_categories(request):
    return render(request, 'course/course-categories.html')

def course_detail(request):
    return render(request, 'course/course-detail.html')