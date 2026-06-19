from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'website/index.html')

def contact(request):
    return render(request, 'website/contact.html')

def about(request):
    return render(request, 'website/about.html')

def faq(request):
    return render(request, 'website/faq.html')

def error_404(request):
    return render(request, 'website/error-404.html')