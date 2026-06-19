from django.shortcuts import render

# Create your views here.
def sign_in(request):
    return render(request, "authentication/sign-in.html")

def sign_up(request):
    return render(request, "authentication/sign-up.html")

def forgot_password(request):
    return render(request, "authentication/forgot-password.html")