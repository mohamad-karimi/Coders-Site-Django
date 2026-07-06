from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from website.form import ContactForm, QuestionForm
from course.models import Course, Score
from blog.models import Post
from itertools import chain
from website.models import Question, Answer, MentorUser, QuestionLike, CATEGORY_CHOICES
from instructor.models import Instructor
from django.db.models import Avg, Count, Q
from django.utils import timezone
from instructor.models import Instructor
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
from coders import settings

User = get_user_model()

# Create your views here.
def index(request):
    course = Course.objects.prefetch_related('sections__lessons').annotate(
        avg_score=Avg('score__score')
    )
    mentorusers = MentorUser.objects.all()
    instructor = Instructor.objects.all
    total_students = User.objects.all().count()
    total_courses_with_certification = course.filter(certification="بله").count()

    overall_avg = course.aggregate(
        overall=Avg('avg_score')
    )['overall'] or 0
    overall_avg = round(overall_avg * 2) / 2
    full = int(overall_avg)
    has_half = (overall_avg - full) >= 0.5
    empty = 5 - full - int(has_half)

    total_scores = Score.objects.count()
    users = User.objects.all()

    context = {
        "course" : course,
        "users" : users,
        "mentorusers" : mentorusers,
        "total_students" : total_students,
        "instructor" : instructor,
        "total_courses_with_certification" : total_courses_with_certification,
        "overall_avg" : overall_avg,
        "total_scores" : total_scores,
        "full": range(full),
        "half": has_half,
        "empty": range(empty),
    }
    return render(request, 'website/index.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        token = request.POST.get("cf-turnstile-response")

        if not verify_turnstile(token, request):
            messages.error(request, "تأیید امنیتی نامعتبر است")
            return render(request, 'website/contact.html', {"form": form})

        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما ارسال شد")
            return redirect('website:home')
        else:
            messages.error(request, "اطلاعات فرم صحیح نیست")

    else:
        form = ContactForm()

    return render(request, 'website/contact.html', {"form": form})

def about(request):
    instructors = Instructor.objects.annotate(
        avg_score=Avg('courses__score__score')
    )

    for obj in instructors:
        avg = obj.avg_score or 0 

        obj.full = int(avg)
        obj.half = (avg - obj.full) >= 0.5
        obj.empty = 5 - obj.full - int(obj.half)

    context = {
        "instructors" : instructors,
        }
    return render(request, 'website/about.html', context)

def faq(request):
    courses = Course.objects.prefetch_related('tag').all()
    posts = Post.objects.prefetch_related('tag').all()
    questions = Question.objects.filter(published=True).order_by('-created_date').annotate(
        like_count=Count('questionLike')
    )
    category = request.GET.get('category') 
    
    if category:
        questions = questions.filter(category=category)

    course_tags = list(chain.from_iterable(c.tag.all() for c in courses))[:5]
    post_tags = list(chain.from_iterable(p.tag.all() for p in posts))[:5]
    raw_counts = (
        Question.objects.values('category')
        .annotate(count=Count('id'))
    )

    count_map = {c['category']: c['count'] for c in raw_counts}

    categories = [
        {
            "value": key,
            "label": label,
            "count": count_map.get(key, 0)
        }
        for key, label in CATEGORY_CHOICES
    ]

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'questions':
            form = QuestionForm(request.POST)

            if form.is_valid():
                question_obj = form.save(commit=False)
                question_obj.name = request.user
                question_obj.save()

                messages.success(request, "سوال شما ارسال شد منتظر پاسخ باشید")
                return redirect('website:faq')  
            else:
                messages.error(request, "اطلاعات فرم صحیح نیست")
        
        elif form_type == 'reply':
            reply_text = request.POST.get('answer')
            question_id = request.POST.get('question_id')

            if reply_text and question_id:
                Answer.objects.create(
                    question_id=question_id,
                    text=reply_text,
                    name=request.user,
                    parent=None
                )
                messages.success(request, "پاسخ ثبت شد")
                return redirect('website:faq')
            else:
                messages.error(request, "اطلاعات فرم صحیح نیست")

    latest_question = Question.objects.first()
    questions_count = Question.objects.count()
    answers_count = Answer.objects.count()

    context = {
        "course_tags": course_tags,
        "post_tags": post_tags,
        "questions": questions, 
        "latest_question" : latest_question,
        "questions_count" : questions_count,
        "answers_count" : answers_count,
        "categories" : categories,
        "questions_count" : questions_count,
    }

    return render(request, 'website/faq.html', context)

def error_404(request, exception):
    return render(request, 'website/error-404.html', status = 404)

def search(request):
    courses = Course.objects.filter(
        status=True, published_date__lte=timezone.now())
    if request.method == "GET":
        if s := request.GET.get("s"):
            courses = courses.filter(Q(title__icontains=s) |
                                 Q(short_description__icontains=s))
    context = {"courses": courses}
    return render(request, "course/course-list.html", context)

@login_required
def like_question(request, id):

    question = get_object_or_404(Question, id=id)

    like, created = QuestionLike.objects.get_or_create(
        user=request.user,
        question=question
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "count": question.questionLike.count()
    })

def verify_turnstile(token, request):
    response = requests.post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data={
            "secret": settings.TURNSTILE_SECRET_KEY,
            "response": token,
            "remoteip": request.META.get("REMOTE_ADDR"),
        }
    )

    return response.json().get("success", False)