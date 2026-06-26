from course.models import CourseProgress, LessonProgress, Score, Course
from django.db.models import Q
from django.db.models import Avg

def dashboard_context(request):
    if not request.user.is_authenticated:
        return {}
    
    courses = Course.objects.filter(
        status=True,
        enrollment__user=request.user
    ).distinct().annotate(
        avg_score=Avg('score__score')
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

    completed_lessons = LessonProgress.objects.filter(
        user=request.user,
        is_completed=True
    ).count()

    completed_courses = CourseProgress.objects.filter(
        user=request.user,
        is_completed=True
    ).count()

    return {
        "courses" : courses,
        "completed_lessons" : completed_lessons,
        "total_scores" : total_scores,
        "completed_courses" : completed_courses,
    }