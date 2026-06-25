from django.shortcuts import render
from instructor.models import Instructor
from django.shortcuts import render, get_object_or_404
from course.models import Course, Enrollment
from django.db.models import Avg
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

# Create your views here.
def IN_list(request):
    instructor = Instructor.objects.annotate(
    avg_score=Avg('courses__score__score')
    )

    experts = Instructor.objects.values_list("expertise", flat=True).distinct()

    expertise = request.GET.get("expertise")
    if expertise:
        instructor = instructor.filter(expertise=expertise)

    sort = request.GET.get("sort")
    if sort == "scores":
        instructor = instructor.order_by("-avg_score")

    elif sort == "views":
        instructor = instructor.order_by("-counted_views")

    print(Instructor.objects.values_list("expertise", flat=True))
    paginator = Paginator(instructor, 6)
    try:
        page_number = request.GET.get("page")
        instructor = paginator.get_page(page_number)
    except PageNotAnInteger:
        instructor = paginator.get_page(1)
    except EmptyPage:
        instructor = paginator.get_page(paginator.num_pages)
    
    context = {
        "instructor":instructor,
        "experts" : experts,
        }
    return render(request, 'instructor/instructor-list.html', context)


def IN_single(request, slug):
    instructor = get_object_or_404(
        Instructor.objects.prefetch_related('educations', 'skills'),
        slug=slug
    )

    instructor.counted_views += 1
    instructor.save(update_fields=['counted_views'])

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

    total_students = Enrollment.objects.filter(
        course__instructor=instructor
    ).count()

    context = {
        "instructor": instructor,
        "instructors": instructors,  
        "courses": courses,
        "total_students" : total_students,
        "num_courses": instructor.courses.count(),
        "full": range(full),
        "half": has_half,
        "empty": range(empty),
    }

    return render(request, 'instructor/instructor-single.html', context)

def instructor_search(request):
    instructor = Instructor.objects.all()

    if request.method == "GET":
        if s := request.GET.get("s"):
            instructor = instructor.filter(Q(name__icontains=s))

    context = {"instructor": instructor}
    return render(request, "instructor/instructor-list.html", context)