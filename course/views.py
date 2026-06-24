from django.shortcuts import render
from course.models import Course, ReplayComment, Enrollment, Comment, Category
from django.shortcuts import render, get_object_or_404
import jdatetime
from course.form import ScoreForm, CommentForm
from django.shortcuts import render
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.db.models import Avg
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.db.models import Count

# Create your views here.
def course_list(request, **kwargs):
    courses = Course.objects.filter(status=True).annotate(
        avg_score=Avg('score__score')
    )
    if kwargs.get("ca_name") != None:
        courses = courses.filter(category__name=kwargs["ca_name"])
        
    if kwargs.get("ta_name"):
        courses = courses.filter(tag__name__iexact=kwargs["ta_name"]).distinct()

    if kwargs.get("sk_name") is not None:
        courses = courses.filter(skill_level=kwargs["sk_name"])

    paginator = Paginator(courses, 3)
    try:
        page_number = request.GET.get("page")
        courses = paginator.get_page(page_number)
    except PageNotAnInteger:
        courses = paginator.get_page(1)
    except EmptyPage:
        courses = paginator.get_page(paginator.num_pages)

    context = {
        "courses": courses,
    }
    return render(request, 'course/course-list.html', context)

def course_categories(request):
    category = Category.objects.annotate(
        course_count=Count('courses')
    )

    context = {
        "category": category,
    }
    return render(request, 'course/course-categories.html', context)

def course_detail(request, slug):
    course = get_object_or_404(
        Course.objects.prefetch_related('sections__lessons'),
        slug=slug
    )

    course.published_jalali = jdatetime.datetime.fromgregorian(
        datetime=course.published_date
    ).strftime("%Y/%m/%d")


    courses = Course.objects.all()
    comment = course.comment.all()
    scores = course.score.all()

    for s in scores:
        avg = s.score

        s.full = int(avg)
        s.half = (avg - s.full) >= 0.5
        s.empty = 5 - s.full - int(s.half)

    if request.method == 'POST':

        form_type = request.POST.get('form_type')

        if form_type == 'score':
            form = ScoreForm(request.POST)

            if form.is_valid():
                try:
                    score_obj = form.save(commit=False)
                    score_obj.course = course
                    score_obj.user = request.user
                    score_obj.save()

                    messages.success(request, "نظر شما ثبت شد")
                    return redirect('course:course_detail', slug=slug)

                except IntegrityError:
                    messages.error(request, "شما قبلاً امتیاز داده‌اید")
            else:
                messages.error(request, "اطلاعات فرم صحیح نیست")
        elif form_type == 'comment':
            form = CommentForm(request.POST)

            if form.is_valid():
                comment_obj = form.save(commit=False)
                comment_obj.author = request.user
                comment_obj.course = course
                comment_obj.save()

                messages.success(request, "کامنت شما ثبت شد")
                return redirect('course:course_detail', slug=slug)
            else:
                messages.error(request, "اطلاعات فرم صحیح نیست")
        elif form_type == 'reply':
            reply_text = request.POST.get('comment')
            parent_id = request.POST.get('parent_id')

            if reply_text and parent_id:
                ReplayComment.objects.create(
                    author=request.user,
                    comment=reply_text,
                    question_comment_id=int(parent_id)
                )
                messages.success(request, "کامنت شما ثبت شد")
                return redirect('course:course_detail', slug=slug)
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

    instructor = course.instructor
    total_students = Enrollment.objects.filter(
        course__instructor=instructor
    ).count()
    total_comments = Comment.objects.filter(
        course__instructor=instructor
    ).count()
    
    remaining_days = None
    if course.discount_end:
        remaining_days = (course.discount_end - timezone.now()).days

    context = {
        "course": course,
        "courses": courses,
        "scores": scores,
        "comment": comment,
        "total_students" : total_students,
        "total_comments" : total_comments,
        "remaining_days": remaining_days,
        "avg_score": avg_score,
        "full": range(full),
        "half": 1 if has_half else 0,
        "empty": range(empty),
        "rows": rows,
        }
    return render(request, 'course/course-detail.html', context)