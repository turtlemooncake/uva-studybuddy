from http.client import HTTPResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Profile, Course
from .forms import ProfileForm
from django.contrib.auth import logout


def home(request):
    return render(request, 'home.html')

def login(request):
    if request.user.is_authenticated and not (Profile.objects.filter(user_id=request.user.id)).exists():
        return HttpResponseRedirect(reverse('register'))
    return render(request, 'index.html')


def register(request):
    form = ProfileForm(request.POST) 
    if Profile.objects.filter(user_id=request.user.id).exists() and request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if (form.is_valid()):
        preferredName = request.POST['user']
        request.user.username = preferredName
        print(request.user.username)
        request.user.save()

        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()

        return HttpResponseRedirect(reverse('addCourses'))
    
    context = {
        'form': form
    }
       
    return render(request, 'registerProfile.html', context)

def profile(request):
    theUser = Profile.objects.get(user_id=request.user.id)
    return render(request, 'profile.html', {"user" : theUser})

def addCourses(request):
    allCourses = Course.objects.all() 
    theUser = Profile.objects.get(user_id=request.user.id)
    
    if request.method == 'POST':
        if 'Filter' in request.POST:
            allCourses = Course.objects.filter(courseAbbv=request.POST['courseAb'])

        if 'Add Course' in request.POST:    
            if (Course.objects.filter(courseAbbv=request.POST['courseAb']).exists() and Course.objects.filter(courseNumber=request.POST['courseNumb']).exists()): 
                theUser.courses.add(Course.objects.get(courseAbbv=request.POST['courseAb'], courseNumber=request.POST['courseNumb']))
                print('course added to current user')
        
        print('in post expression')
    else:
        allCourses = Course.objects.all()
    
    context = {
        'allCourses' : allCourses
    }
    
    return render(request, 'addCourses.html', context)

def logOut(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    logout(request)
    
    return render(request, 'index.html')

class ProfileList(generic.ListView):
    model = Profile
    context_object_name = 'profileList'
    template_name = 'findBuddies.html'

    def get_queryset(self):
        return Profile.objects.all()