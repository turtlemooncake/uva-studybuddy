from http.client import HTTPResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import ProfileForm

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

    
    context = {
        'form': form
    }
       
    return render(request, 'registerProfile.html', context)

def profile(request):
    theUser = Profile.objects.get(user_id=request.user.id)
    return render(request, 'profile.html', {"user" : theUser})

def calendar(request):
    return render(request, 'calendar.html')
