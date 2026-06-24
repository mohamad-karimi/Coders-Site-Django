from django import template
from course.models import Course
from django.utils import timezone
from django.db.models import Count
from django.db.models import Avg

register = template.Library()

@register.inclusion_tag('website/popular_course.html')
def popular_course(count=8):
    courses = Course.objects.filter(
        status=True,
        published_date__lte=timezone.now()
    ).annotate(
        avg_score=Avg("score__score")
    )

    def add_rating(course):
        avg = course.avg_score or 0
        course.full = int(avg)
        course.half = (avg - course.full) >= 0.5
        course.empty = 5 - course.full - int(course.half)
        return course
    
    def get_courses(category_name):
        return [
            add_rating(c)
            for c in courses.filter(category__name=category_name)
            .order_by("-avg_score")[:count]
        ]
    
    courses_web_design = get_courses("طراحی وب")
    courses_development = get_courses("توسعه وب")
    courses_graphic_design = get_courses("طراحی گرافیک")
    courses_marketing = get_courses("بازاریابی")
    courses_financial_affairs = get_courses("امور مالی")

    return {
        "courses_web_design": courses_web_design,
        "courses_development": courses_development,
        "courses_graphic_design": courses_graphic_design,
        "courses_marketing": courses_marketing,
        "courses_financial_affairs": courses_financial_affairs,
        }