from course.models import CourseProgress, LessonProgress, Score

def user_stats(request):
    if not request.user.is_authenticated:
        return {}

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
        "completed_lessons" : completed_lessons,
        "total_scores" : total_scores,
        "completed_courses" : completed_courses,
    }