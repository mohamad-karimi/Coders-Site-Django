from django.shortcuts import render
from course.models import Course
from django.shortcuts import render, get_object_or_404
import jdatetime

# Create your views here.
def course_list(request):
    course = Course.objects.select_related('instructor').filter(status=True)

    context = {"course":course}
    return render(request, 'course/course-list.html', context)

def course_categories(request):
    return render(request, 'course/course-categories.html')

def course_detail(request, slug):
    course = get_object_or_404(
        Course.objects.prefetch_related(
            'sections__lessons'
        ),
        slug=slug
    )
    course.jalali_date = jdatetime.datetime.fromgregorian(datetime=course.updated_date)
    course.jalali_date_formatted = course.jalali_date.strftime("%Y/%m/%d")

    courses = Course.objects.all()

    context = {"course": course,
               "courses": courses,
               }
    return render(request, 'course/course-detail.html', context)