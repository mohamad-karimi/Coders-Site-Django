from django import template
from course.models import Course
from django.utils import timezone
from django.db.models import Avg

register = template.Library()

@register.inclusion_tag('course/course_latest.html')
def latest_course(count=2):
    course = Course.objects.filter(status = True,  published_date__lte = timezone.now()).order_by("-published_date")[:count].annotate(
        avg_score=Avg('score__score')
    )
    return {"course" : course}

@register.inclusion_tag('course/top_course.html')
def top_course(count=4):
    course = Course.objects.filter(status = True,  published_date__lte = timezone.now()).order_by("-published_date")[:count].annotate(
        avg_score=Avg('score__score')
    )
    return {"course" : course}
