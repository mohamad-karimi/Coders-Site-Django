from django.shortcuts import render, redirect
from authentication.form import CustomLoginForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model, logout, login
import requests
from django.contrib.auth.decorators import login_required
from django.conf import settings

User = get_user_model()

# Create your views here.
def verify_recaptcha(token, remote_ip):
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": settings.RECAPTCHA_SECRET_KEY,
        "response": token,
        "remoteip": remote_ip,
    }
    response = requests.post(url, data=data)
    result = response.json()
    return result

def sign_in(request):
    if not request.user.is_authenticated:
        form = CustomLoginForm(request, data=request.POST or None)
        form.fields['username'].widget.attrs.update({
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': 'mohamad'
        })

        form.fields['password'].widget.attrs.update({
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': '*********'
        })
        if request.method == "POST":

            token = request.POST.get("recaptcha_token")
            if not token:
                messages.error(request, "توکن کپچا ارسال نشده")
                return redirect("authentication:login")
    
            result = verify_recaptcha(token, request.META.get("REMOTE_ADDR"))

            if not result.get("success"):
                messages.error(request, "reCAPTCHA نامعتبر است")
                return redirect("authentication:login")

            score = result.get("score", 0)

            if score < 0.5:
                messages.error(request, "رفتار شما مشکوک تشخیص داده شد")
                return redirect("authentication:login")
            
            if form.is_valid():
                login(request, form.get_user())

                if request.POST.get('remember_me'):
                  request.session.set_expiry(60 * 60 * 24 * 30)
                else:
                    request.session.set_expiry(0)

                return redirect("/")

        total_student = User.objects.all().count()
        users = User.objects.all()

        context = {
            'form':form,
            "users" : users,
            "total_student" : total_student,
            "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY
            }
        return render(request, 'authentication/sign-in.html', context)
    else:
        return redirect("/")
    
def sign_up(request):
    if not request.user.is_authenticated:
        form = CustomUserCreationForm(request.POST or None, request.FILES or None)
        form.fields['username'].widget.attrs.update({
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': 'mohamad'
        })

        form.fields['email'].widget.attrs.update({
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': 'example@gmail.com'
        })

        form.fields['password1'].widget.attrs.update({
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': '*********'
        })
        form.fields['password2'].widget.attrs.update({
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': '*********'
        })

        if request.method == "POST":

            token = request.POST.get("recaptcha_token")
            if not token:
                messages.error(request, "توکن کپچا ارسال نشده")
                return redirect("authentication:login")
    
            result = verify_recaptcha(token, request.META.get("REMOTE_ADDR"))

            if not result.get("success"):
                messages.error(request, "reCAPTCHA نامعتبر است")
                return redirect("authentication:login")

            score = result.get("score", 0)

            if score < 0.5:
                messages.error(request, "رفتار شما مشکوک تشخیص داده شد")
                return redirect("authentication:login")
        
            if form.is_valid():
                form.save()
                messages.success(request, "اکانت با موفقیت ساخته شد")
                return redirect("authentication:login")
            else:
                messages.error(request, "اطلاعات فرم نادرست است")
        
        total_student = User.objects.all().count()
        users = User.objects.all()

        context = {
            'form':form,
            "users" : users,
            "total_student" : total_student,
            "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY
            }
        return render(request, 'authentication/sign-up.html', context)
    else:
        return redirect("/")
    
@login_required
def logout_view(request):
    logout(request)
    return redirect("/")
        
def verify_recaptcha_v3(token, request):
    url = "https://www.google.com/recaptcha/api/siteverify"

    data = {
        "secret": settings.RECAPTCHA_V3_SECRET_KEY,
        "response": token,
        "remoteip": request.META.get("REMOTE_ADDR"),
    }

    response = requests.post(url, data=data)
    result = response.json()

    return result.get("success", False) and result.get("score", 0) >= 0.5