from http.client import HTTPResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Profile
from .models import StudySession
from .forms import ProfileForm
from .forms import SessionForm

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


def session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)

        if form.is_valid():
            session = StudySession()
            #session.users = request.user.objects.values_list('username', flat='True')
            session.save()
            session.users.add(request.POST.get('users'))
            session.date = request.POST.get('date')
            session.time = request.POST.get('time')
            session.location = request.POST.get('location')
            session.subject = request.POST.get('subject')
            session.save()
            return render(request, 'sessions.html', {'session': session})
    else:
        form = SessionForm()

    return render(request, 'newSession.html', {'form': form})

def profile(request):
    theUser = Profile.objects.get(user_id=request.user.id)
    return render(request, 'profile.html', {"user" : theUser})

