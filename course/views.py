from django.shortcuts import render
from course.models import Course
from django.shortcuts import render, get_object_or_404
import jdatetime
from course.form import ScoreForm
from django.shortcuts import render
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.db.models import Avg

# Create your views here.
def course_list(request):
    course = Course.objects.filter(status=True).annotate(
        avg_score=Avg('score__score')
    )

    context = {
        "course": course,
    }
    return render(request, 'course/course-list.html', context)

def course_categories(request):
    return render(request, 'course/course-categories.html')

def course_detail(request, slug):
    course = get_object_or_404(
        Course.objects.prefetch_related('sections__lessons'),
        slug=slug
    )

    course.published_jalali = jdatetime.datetime.fromgregorian(
        datetime=course.published_date
    ).strftime("%Y/%m/%d")


    courses = Course.objects.all()
    scores = course.score.all()

    form = ScoreForm()

    if request.method == 'POST':
        form = ScoreForm(request.POST)

        if form.is_valid():
            try:
                score_obj = form.save(commit=False)
                score_obj.course = course
                score_obj.save()

                messages.success(request, "نظر شما ثبت شد")

                return redirect('course:course_detail', slug=slug)

            except IntegrityError:
                messages.error(request, "شما قبلاً نظر داده‌اید")
        else:
            messages.error(request, "اطلاعات فرم صحیح نیست")

    avg_score = course.score.aggregate(avg=Avg('score'))['avg'] or 0
    full = int(avg_score)
    has_half = (avg_score - full) >= 0.5
    empty = 5 - full - int(has_half)

    total = scores.count() 
    rows = []

    for star in range(5, 0, -1):
        count = scores.filter(score=star).count()
        percent = (count / total * 100) if total else 0

        rows.append({
            "star": star,
            "percent": percent
        })

    context = {
        "course": course,
        "courses": courses,
        "scores": scores,
        "avg_score": avg_score,
        "full": range(full),
        "half": 1 if has_half else 0,
        "empty": range(empty),
        "rows": rows,
        }
    return render(request, 'course/course-detail.html', context)