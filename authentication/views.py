from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from authentication.form import CustomLoginForm, CustomUserCreationForm
from django.contrib import messages
import json
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

User = get_user_model()

# Create your views here.
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
            if form.is_valid():
                login(request, form.get_user())

                if request.POST.get('remember_me'):
                  request.session.set_expiry(60 * 60 * 24 * 30)
                else:
                    request.session.set_expiry(0)

                return redirect("/")

        context = {'form':form}
        return render(request, 'authentication/sign-in.html', context)
    else:
        return redirect("/")
    
def sign_up(request):
    if not request.user.is_authenticated:
        form = CustomUserCreationForm(data=request.POST or None)
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
            print(form.errors)
            if form.is_valid():
                form.save()
                messages.success(request, "Account created successfully")
                return redirect("authentication:login")
            else:
                messages.error(request, "Please correct the errors below")
        
        context = {'form':form}
        return render(request, 'authentication/sign-up.html', context)
    else:
        return redirect("/")
    
@login_required
def logout_view(request):
    logout(request)
    return redirect("/")

def google_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        token = data.get("credential")

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                "321149008744-8agt4hkkao5abome759eg67gpl2ns49a.apps.googleusercontent.com"
            )

            email = idinfo["email"]
            name = idinfo.get("name", email.split("@")[0])
            picture = idinfo.get("picture")

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": name
                }
            )

            login(request, user)

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
        
def forgot_password(request):
    return render(request, 'authentication/forgot-password.html')