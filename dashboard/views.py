from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from course.models import Course, CourseProgress
from dashboard.form import EditProfileForm, EmailForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

# Create your views here.
@login_required
def dashboard(request):
    courses_count = Course.objects.all().count()

    certificates_count = CourseProgress.objects.filter(
        user=request.user,
        certificate_received=True
    ).count()

    context = {
        "courses_count": courses_count,
        "certificates_count": certificates_count,
    }

    return render(request, 'dashboard/student-dashboard.html', context)

def course_list(request):
    return render(request, 'dashboard/student-course-list.html')

def course_resume(request):
    return render(request, 'dashboard/student-course-resume.html')

@login_required
def edit_profile(request):

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
                return redirect("dashboard:edit_profile")

        elif request.POST.get("form_type") == "email":
            email_form = EmailForm(
                request.POST,
                instance=request.user
            )

            if email_form.is_valid():
                email_form.save()
                messages.success(request, "ایمیل بروزرسانی شد.")
                return redirect("dashboard:edit_profile")

        elif request.POST.get("form_type") == "password":
            password_form = PasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                user = request.user
                user.set_password(password_form.cleaned_data["new_password"])
                user.save()

                update_session_auth_hash(request, user)

                messages.success(request, "رمز عبور تغییر کرد")
                return redirect("dashboard:edit_profile")

    return render(request, "dashboard/edit-profile.html", {
        "profile_form": profile_form,
        "email_form": email_form,
        "password_form": password_form
    })

@login_required
def delete_account(request):
    if request.method == "GET":
        request.user.delete()
        return redirect("/")

    return redirect("dashboard:dashboard")