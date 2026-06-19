from django.shortcuts import render

# Create your views here.
def IN_list(request):
    return render(request, 'instructor/instructor-list.html')

def IN_single(request):
    return render(request, 'instructor/instructor-single.html')