from django.shortcuts import render
from instructor.models import Instructor

# Create your views here.
def IN_list(request):
    instructor = Instructor.objects.all()

    context = {"instructor":instructor}
    return render(request, 'instructor/instructor-list.html', context)

def IN_single(request):
    return render(request, 'instructor/instructor-single.html')