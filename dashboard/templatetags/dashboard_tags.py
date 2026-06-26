from django import template
from django.db.models import Count, Q
from course.models import LessonProgress

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