from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from website.form import ContactForm, QuestionForm
from course.models import Course
from blog.models import Post
from itertools import chain
from website.models import Question, Answer
from django.db.models import Count
from website.models import CATEGORY_CHOICES

# Create your views here.
def index(request):
    return render(request, 'website/index.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "پیام شما ارسال شد")
            return redirect('website:home')
        else:
            messages.error(request, "اطلاعات فرم صحیح نیست")

    return render(request, 'website/contact.html')

def about(request):
    return render(request, 'website/about.html')

def faq(request):
    courses = Course.objects.prefetch_related('tag').all()
    posts = Post.objects.prefetch_related('tag').all()
    questions = Question.objects.all().order_by('-created_date')
    category = request.GET.get('category') 
    
    if category:
        questions = questions.filter(category=category)

    course_tags = list(chain.from_iterable(c.tag.all() for c in courses))
    post_tags = list(chain.from_iterable(p.tag.all() for p in posts))
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
    print(Question)
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

def error_404(request):
    return render(request, 'website/error-404.html')