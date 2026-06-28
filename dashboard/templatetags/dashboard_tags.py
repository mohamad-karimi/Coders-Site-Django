from course.models import LessonProgress
from django import template

register = template.Library()


@register.simple_tag
def section_completed_lessons(section, user):
    return LessonProgress.objects.filter(
        lesson__section=section,
        user=user,
        is_completed=True
    ).count()

@register.simple_tag
def is_lesson_completed(lesson, user):
    return LessonProgress.objects.filter(
        lesson=lesson,
        user=user,
        is_completed=True
    ).exists()

@register.simple_tag
def section_progress(section, user):
    total = section.lessons.count()

    if total == 0:
        return 0

    completed = section.lessons.filter(
        progress__user=user,
        progress__is_completed=True
    ).count()

    return (completed / total) * 100