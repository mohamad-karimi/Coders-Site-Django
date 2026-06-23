from django.shortcuts import render
from instructor.models import Instructor
from django.shortcuts import render, get_object_or_404
from course.models import Course
from django.db.models import Avg

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

    instructors = Instructor.objects.annotate(
        avg_score=Avg('courses__score__score')
    )

    for obj in instructors:
        avg = obj.avg_score or 0 

        obj.full = int(avg)
        obj.half = (avg - obj.full) >= 0.5
        obj.empty = 5 - obj.full - int(obj.half)

    courses = Course.objects.filter(instructor=instructor).annotate(
    avg_score=Avg('score__score')
    )
    for course_obj in courses:
        avg = course_obj.avg_score or 0 

        course_obj.full = int(avg)
        course_obj.half = (avg - course_obj.full) >= 0.5
        course_obj.empty = 5 - course_obj.full - int(course_obj.half)

    avg_score = instructor.instructor_avg_score or 0

    full = int(avg_score)
    has_half = (avg_score - full) >= 0.5
    empty = 5 - full - int(has_half)

    context = {
        "instructor": instructor,
        "instructors": instructors,  
        "courses": courses,
        "num_courses": instructor.courses.count(),
        "full": range(full),
        "half": has_half,
        "empty": range(empty),
    }

    return render(request, 'instructor/instructor-single.html', context)