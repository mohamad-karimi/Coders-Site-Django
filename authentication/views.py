from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from authentication.form import CustomLoginForm

# Create your views here.
def sign_in(request):
    if not request.user.is_authenticated:
        form = CustomLoginForm(request, data=request.POST or None)
        form.fields['username'].widget.attrs.update({
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': 'ایمیل یا نام کاربری'
        })

        form.fields['password'].widget.attrs.update({
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': 'رمز عبور'
        })
        if request.method == "POST":
            if form.is_valid():
                login(request, form.get_user())
                return redirect("/")

        context = {'form':form}
        return render(request, 'authentication/sign-in.html', context)
    else:
        return redirect("/")
    
def sign_up(request):
    return render(request, "authentication/sign-up.html")

def forgot_password(request):
    return render(request, 'authentication/forgot-password.html')