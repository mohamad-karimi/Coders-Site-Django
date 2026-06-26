from course.models import CourseProgress, LessonProgress, Score, Course
from django.db.models import Count, Q
from django.db.models import Count, Q, FloatField
from django.db.models.functions import Cast
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def dashboard_context(request):
    if not request.user.is_authenticated:
        return {}
    
    courses = Course.objects.filter(
        status=True,
        enrollment__user=request.user
    ).annotate(
        completed_lessons=Count(
            "sections__lessons__progress",
            filter=Q(
                sections__lessons__progress__user=request.user,
                sections__lessons__progress__is_completed=True,
            ),
            distinct=True,
        ),
    ).annotate(
        progress_percent=Cast(
            100.0 * Count(
                "sections__lessons__progress",
                filter=Q(
                    sections__lessons__progress__user=request.user,
                    sections__lessons__progress__is_completed=True,
                ),
                distinct=True,
            )
            / Count("sections__lessons", distinct=True),
            FloatField()
        )
    ) 

    s = request.GET.get("s")
    if s:
        courses = courses.filter(
            Q(title__icontains=s) |
            Q(overview__icontains=s)
        )

    sort = request.GET.get("sort")
    if sort == "free":
        courses = courses.filter(is_free=True)

    elif sort == "newest":
        courses = courses.order_by("-created_date")

    elif sort == "popular":
        courses = courses.order_by("-avg_score")

    elif sort == "views":
        courses = courses.order_by("-counted_views")

    total_scores = Score.objects.filter(
        user=request.user
    ).count()

    total_completed_lessons = LessonProgress.objects.filter(
        user=request.user,
        is_completed=True
    ).count()

    completed_courses = CourseProgress.objects.filter(
        user=request.user,
        is_completed=True
    ).count()

    paginator = Paginator(courses, 4)
    try:
        page_number = request.GET.get("page")
        courses = paginator.get_page(page_number)
    except PageNotAnInteger:
        courses = paginator.get_page(1)
    except EmptyPage:
        courses = paginator.get_page(paginator.num_pages)

    return {
        "courses" : courses,
        "paginator": paginator,
        "total_completed_lessons" : total_completed_lessons,
        "total_scores" : total_scores,
        "completed_courses" : completed_courses,
    }