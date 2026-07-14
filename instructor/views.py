from django.shortcuts import render, render, get_object_or_404, redirect
from instructor.models import Instructor
from course.models import Course, Enrollment, Section, Purchase
from django.db.models import Avg, Q, Sum
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from dashboard.form import EditProfileForm, EmailForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from instructor.form import CourseForm, SectionForm, LessonForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import jdatetime
import json

User = get_user_model()

# Create your views here.
def IN_list(request):
    instructor = Instructor.objects.annotate(
    avg_score=Avg('courses__score__score')
    )

    experts = Instructor.objects.values_list("expertise", flat=True).distinct()

    expertise = request.GET.get("expertise")
    if expertise:
        instructor = instructor.filter(expertise=expertise)

    sort = request.GET.get("sort")
    if sort == "scores":
        instructor = instructor.order_by("-avg_score")

    elif sort == "views":
        instructor = instructor.order_by("-counted_views")

    print(Instructor.objects.values_list("expertise", flat=True))
    paginator = Paginator(instructor, 6)
    try:
        page_number = request.GET.get("page")
        instructor = paginator.get_page(page_number)
    except PageNotAnInteger:
        instructor = paginator.get_page(1)
    except EmptyPage:
        instructor = paginator.get_page(paginator.num_pages)
    
    context = {
        "instructor":instructor,
        "experts" : experts,
        }
    return render(request, 'instructor/instructor-list.html', context)


def IN_single(request, slug):
    instructor = get_object_or_404(
        Instructor.objects.prefetch_related('educations', 'skills'),
        slug=slug
    )

    instructor.counted_views += 1
    instructor.save(update_fields=['counted_views'])

    instructors = Instructor.objects.annotate(
        avg_score=Avg('courses__score__score')
    )

    for obj in instructors:
        avg = obj.avg_score or 0 

        obj.full = int(avg)
        obj.half = (avg - obj.full) >= 0.5
        obj.empty = 5 - obj.full - int(obj.half)

    courses = Course.objects.filter(instructor=instructor).annotate(
    avg_score=Avg('score__score')
    )
    for course_obj in courses:
        avg = course_obj.avg_score or 0 

        course_obj.full = int(avg)
        course_obj.half = (avg - course_obj.full) >= 0.5
        course_obj.empty = 5 - course_obj.full - int(course_obj.half)

    avg_score = instructor.instructor_avg_score or 0

    full = int(avg_score)
    has_half = (avg_score - full) >= 0.5
    empty = 5 - full - int(has_half)

    total_students = Enrollment.objects.filter(
        course__instructor=instructor
    ).count()

    context = {
        "instructor": instructor,
        "instructors": instructors,  
        "courses": courses,
        "total_students" : total_students,
        "num_courses": instructor.courses.count(),
        "full": range(full),
        "half": has_half,
        "empty": range(empty),
    }

    return render(request, 'instructor/instructor-single.html', context)

def instructor_search(request):
    instructor = Instructor.objects.all()

    if request.method == "GET":
        if s := request.GET.get("s"):
            instructor = instructor.filter(Q(name__icontains=s))

    context = {"instructor": instructor}
    return render(request, "instructor/instructor-list.html", context)

@login_required
def dashboard(request):
    if request.user.role != User.Role.INSTRUCTOR:
        raise PermissionDenied
    
    instructor = request.user.instructor
    courses = Course.objects.filter(instructor=instructor)
    total_courses = Course.objects.filter(instructor=instructor).count()
    students_count = User.objects.filter(
        enrollment__course__instructor=instructor
    ).distinct().count()
    total_student = User.objects.filter(role="student").count()

    now = timezone.localtime()
    start_of_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_last_month = (start_of_this_month - timedelta(days=1)).replace(day=1)

    current_month_total = Purchase.objects.filter(
        course__instructor=instructor,
        created_date__gte=start_of_this_month,
    ).aggregate(total=Sum('amount'))['total'] or 0

    last_month_total = Purchase.objects.filter(
        course__instructor=instructor,
        created_date__gte=start_of_last_month,
        created_date__lt=start_of_this_month,
    ).aggregate(total=Sum('amount'))['total'] or 0

    if last_month_total > 0:
        percent_change = round(
            ((current_month_total - last_month_total) / last_month_total) * 100, 2
        )
    else:
        percent_change = 100 if current_month_total > 0 else 0

    months_labels = []
    months_totals = []

    for i in range(5, -1, -1):
        month_start = (start_of_this_month - relativedelta(months=i))
        if i == 0:
            month_end = now
        else:
            month_end = month_start + relativedelta(months=1)

        total = Purchase.objects.filter(
            course__instructor=instructor,
            created_date__gte=month_start,
            created_date__lt=month_end,
        ).aggregate(total=Sum('amount'))['total'] or 0

        jalali_month = jdatetime.datetime.fromgregorian(datetime=month_start).strftime("%B")
        months_labels.append(jalali_month)
        months_totals.append(total)

    paginator = Paginator(courses, 5)
    try:
        page_number = request.GET.get("page")
        courses = paginator.get_page(page_number)
    except PageNotAnInteger:
        courses = paginator.get_page(1)
    except EmptyPage:
        courses = paginator.get_page(paginator.num_pages)

    context = {
        "instructor":instructor,
        "courses":courses,
        "total_courses":total_courses,
        "students_count":students_count,
        "total_student":total_student,
        "current_month_total": current_month_total,
        "last_month_total": last_month_total,
        "percent_change": percent_change,
        "months_labels": json.dumps(months_labels),
        "months_totals": json.dumps(months_totals),
        "paginator": paginator,
    }
    return render(request, "instructor/instructor-dashboard.html", context)

@login_required
def create_course(request):
    if request.user.role != User.Role.INSTRUCTOR:
        raise PermissionDenied

    instructor = get_object_or_404(Instructor, user=request.user)

    course = Course.objects.filter(instructor=instructor, status=False).order_by('-created_date').first()

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = instructor
            course.save()
            form.save_m2m()
            return redirect("course:course_added", slug=course.slug)
    else:
        form = CourseForm(instance=course)

    return render(request, "instructor/instructor-create-course.html", {
        "form": form,
        "course": course,
    })

@login_required
def delete_account(request):
    if request.method == "GET":
        request.user.delete()
        return redirect("/")

    return redirect("website:home")

@login_required
def edit_profile(request):
    if request.user.role != User.Role.INSTRUCTOR:
        raise PermissionDenied
    
    instructor = request.user.instructor
    total_courses = Course.objects.filter(instructor=instructor).count()
    students_count = User.objects.filter(
        enrollment__course__instructor=instructor
    ).distinct().count()
    total_student = User.objects.filter(role="student").count()
    profile_form = EditProfileForm(instance=request.user)
    email_form = EmailForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":

        if request.POST.get("form_type") == "profile":
            profile_form = EditProfileForm(
                request.POST,
                request.FILES,
                instance=request.user
            )

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "پروفایل ویرایش شد.")
                return redirect("instructor:edit_profile")

        elif request.POST.get("form_type") == "email":
            email_form = EmailForm(
                request.POST,
                instance=request.user
            )

            if email_form.is_valid():
                email_form.save()
                messages.success(request, "ایمیل بروزرسانی شد.")
                return redirect("instructor:edit_profile")

        elif request.POST.get("form_type") == "password":
            password_form = PasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                user = request.user
                user.set_password(password_form.cleaned_data["new_password"])
                user.save()

                update_session_auth_hash(request, user)

                messages.success(request, "رمز عبور تغییر کرد")
                return redirect("instructor:edit_profile")

    return render(request, "instructor/edit-profile.html", {
        "profile_form": profile_form,
        "email_form": email_form,
        "password_form": password_form,
        "instructor":instructor,
        "total_courses":total_courses,
        "students_count":students_count,
        "total_student":total_student,
    })

@login_required
@require_POST
def add_section(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor__user=request.user)
    form = SectionForm(request.POST)
    if form.is_valid():
        section = form.save(commit=False)
        section.course = course
        section.save()
        return JsonResponse({
            "success": True,
            "id": section.id,
            "title": section.title,
        })
    return JsonResponse({"success": False, "errors": form.errors}, status=400)


@login_required
@require_POST
def add_lesson(request, section_id):
    section = get_object_or_404(Section, id=section_id, course__instructor__user=request.user)
    form = LessonForm(request.POST, request.FILES)
    if form.is_valid():
        lesson = form.save(commit=False)
        lesson.section = section
        lesson.save()
        return JsonResponse({
            "success": True,
            "id": lesson.id,
            "title": lesson.title,
        })
    return JsonResponse({"success": False, "errors": form.errors}, status=400)