from django.shortcuts import render
from instructor.models import Instructor
from django.shortcuts import render, get_object_or_404
from course.models import Course
from django.db.models import Count

# Create your views here.
def IN_list(request):
    instructor = Instructor.objects.all()

    context = {"instructor":instructor}
    return render(request, 'instructor/instructor-list.html', context)


def IN_single(request, slug):
    instructor = get_object_or_404(
        Instructor.objects.prefetch_related('educations', 'skills'),
        slug=slug
    )

    instructors = Instructor.objects.all()

    courses = Course.objects.filter(
        instructor=instructor
    )

    num_courses = Course.objects.filter(
        instructor=instructor
    ).count

    context = {
        "instructor": instructor,
        "instructors":instructors,
        "courses": courses,
        "num_courses":num_courses
    }

    return render(request, 'instructor/instructor-single.html', context)