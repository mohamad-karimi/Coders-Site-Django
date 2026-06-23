from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from website.form import contactForm

# Create your views here.
def index(request):
    return render(request, 'website/index.html')

def contact(request):
    if request.method == 'POST':
        form = contactForm(request.POST)

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
    return render(request, 'website/faq.html')

def error_404(request):
    return render(request, 'website/error-404.html')