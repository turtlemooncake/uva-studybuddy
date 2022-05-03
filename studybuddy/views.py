from http.client import HTTPResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django import forms 
from django.contrib import messages

from .models import Profile, Course, StudySession, MessageTwo
from .forms import EditProfileForm, ProfileForm, SessionForm, MessageForm
from django.contrib.auth import logout

from django.conf import settings
from django.http import JsonResponse


def home(request):
    if request.user.is_authenticated and (Profile.objects.filter(user_id=request.user.id)).exists():
        theUser = Profile.objects.get(user_id = request.user.id)
        return render(request, 'home.html', {"user" : theUser})
    return render(request, 'home.html')

def aboutUs(request):
    return render(request, 'aboutUs.html')


def login(request):
    if request.user.is_authenticated and not (Profile.objects.filter(user_id=request.user.id)).exists():
        # theUser = Profile.objects.get(user_id=request.user.id)
        # theUser.picture = "https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
        # theUser.save()
        return HttpResponseRedirect(reverse('register'))
    return HttpResponseRedirect(reverse('home'))


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


def session(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        form = SessionForm(request.POST)

        if form.is_valid():
            new_session = StudySession()
            #session.users = request.user.objects.values_list('username', flat='True')
            new_session.save()
            #session.users.add(request.POST.get('users'))
            temp = request.POST.getlist('users')
            #session.m2mfield.add(*temp)
            new_session.users.add(*temp)
            #return HttpResponse(request.POST.items())
            new_session.creator = request.user
            new_session.date = request.POST.get('date')
            new_session.time = request.POST.get('time')
            new_session.location = request.POST.get('location')
            new_session.subject = request.POST.get('subject')
            new_session.save()
            #return render(request, 'sessions.html', {'session': new_session})
            #return HttpResponseRedirect(reverse('my_sessions', args=(), kwargs={'session': session}))
            #return redirect(my_sessions)
            return HttpResponseRedirect(reverse('my_sessions'))

    else:
        form = SessionForm()

    return render(request, 'newSession.html', {'form': form})

def my_sessions(request):
    showPast = False
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    theUser = Profile.objects.get(user_id=request.user.id)
    allSessions = list(StudySession.objects.filter().all().order_by('created_date'))
    sessions = []
    
    if request.method == 'POST':
        if 'View Past' in request.POST:
            showPast = True
        if 'Hide Past' in request.POST:
            showPast = False
        if 'Delete' in request.POST:
            id = request.POST.get('Delete')
            print(id)
            try:
                selectedSession = StudySession.objects.filter(id=id)[0]
                if selectedSession.creator == theUser.user:
                    try:
                        selectedSession.delete()
                    except:
                        print('This record does not exist')
                else:
                    selectedSession.users.remove(theUser.user)
            except:
                print('There is no such session')


    if not showPast:
        for s in allSessions:
            if(s.date >= datetime.now().astimezone().date):
                sessions.append(s)
    else:   
        sessions = allSessions


    sessions_dict = {
        'sessions': sessions,
        'showPast': showPast,
    }
    return render(request, 'sessions.html', sessions_dict)

def send_message(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            new_message = MessageTwo()
            new_message.sent_by = request.user.username
            new_message.save()
            temp = request.POST.getlist('to')
            new_message.to.add(*temp)
            new_message.message = request.POST.get('message')
            new_message.save()
            return HttpResponseRedirect(reverse('my_messages'))

    else:
        form = MessageForm()

    return render(request, 'newMessage.html', {'form': form})

def my_messages(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    messages = MessageTwo.objects.filter().all().order_by('-created_date')
  
    messages_dict = {
        'messages': messages
    }
    return render(request, 'messages.html', messages_dict)

def profile(request):
    if not request.user.is_authenticated or not (Profile.objects.filter(user_id=request.user.id)).exists():
        return HttpResponseRedirect(reverse('login'))

    theUser = Profile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('editProfile'))

    return render(request, 'profile.html', {"user" : theUser})

def calendar(request):
    return render(request, 'calendar.html')

def addCourses(request):
    if not request.user.is_authenticated or not (Profile.objects.filter(user_id=request.user.id)).exists():
        return HttpResponseRedirect(reverse('login'))
        
    allCourses = Course.objects.all() 
    theUser = Profile.objects.get(user_id=request.user.id)
    courseValid = True
    addedSuccess = False
    dupCourse = False

    if request.method == 'POST':
        if 'Filter' in request.POST:
            if Course.objects.filter(courseAbbv=request.POST['courseAb']).exists(): 
                allCourses = Course.objects.filter(courseAbbv=request.POST['courseAb'])

        if 'Add Course' in request.POST:    
            if (Course.objects.filter(courseAbbv=request.POST['courseAb']).exists() and Course.objects.filter(courseNumber=request.POST['courseNumb']).exists()): 
                if not theUser.courses.filter(courseAbbv=request.POST['courseAb'], courseNumber=request.POST['courseNumb']).exists():
                    theUser.courses.add(Course.objects.get(courseAbbv=request.POST['courseAb'], courseNumber=request.POST['courseNumb']))
                else:
                    dupCourse = True
                courseValid = True
                addedSuccess = True
            else:
                courseValid = False
                addedSuccess - False
                dupCourse = False
        
        if 'Reset Search' in request.POST:
            allCourses = Course.objects.all() 

        else:
            courseA = ""
            courseN = ""
            for courses in allCourses:
                if(request.POST.get(courses.courseAbbv) and request.POST.get(courses.courseAbbv) == courses.courseNumber):
                    courseA = courses.courseAbbv
                    courseN = request.POST.get(courseA)
            if (Course.objects.filter(courseAbbv=courseA).exists() and Course.objects.filter(courseNumber=courseN).exists()): 
                if not theUser.courses.filter(courseAbbv=courseA, courseNumber=courseN).exists():
                    theUser.courses.add(Course.objects.get(courseAbbv=courseA, courseNumber=courseN))
                else:
                    dupCourse = True
                courseValid = True
                addedSuccess = True
            else:
                courseValid = False
                addedSuccess - False
                dupCourse = False
            
        print('in post expression')
    else:
        allCourses = Course.objects.all()
    
    context = {
        'allCourses' : allCourses,
        'courseValid' : courseValid,
        'addedSuccess' : addedSuccess,
        'dupCourse' : dupCourse
    }
    
    return render(request, 'addCourses.html', context)

def logOut(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    logout(request)
    
    return render(request, 'index.html')

def findBuddies(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    allProfiles = Profile.objects.all()

    if request.method == 'POST':
        if 'Reset Search' in request.POST:
            allProfiles = Profile.objects.all()

        if 'Filter Abbr' in request.POST:
            filteredProfiles = []
            foundBoth = False 

            for each in allProfiles:
                if each.courses.filter(courseAbbv=request.POST['courseAb']).exists():
                    filteredProfiles.append(each)
            allProfiles = filteredProfiles

        if 'Filter Num' in request.POST:
            filteredProfiles = []
            foundBoth = False 

            for each in allProfiles:
                if each.courses.filter(courseNumber=request.POST['courseNumb']).exists():
                    filteredProfiles.append(each)
            allProfiles = filteredProfiles

        if 'Filter Name' in request.POST:
            filteredProfiles = []
            foundBoth = False 

            for each in allProfiles:
                if each.user.first_name.lower() == request.POST['firstName'].lower():
                    filteredProfiles.append(each)
            allProfiles = filteredProfiles

        if 'Filter User' in request.POST:
            filteredProfiles = []
            foundBoth = False 

            for each in allProfiles:
                if each.user.username.lower() == request.POST['user'].lower():
                    filteredProfiles.append(each)
            allProfiles = filteredProfiles

        
        if 'Find Buddy' in request.POST:
            filteredProfiles = []
            foundBoth = False 

            for each in allProfiles:
                if each.courses.filter(courseAbbv=request.POST['courseAb'], courseNumber=request.POST['courseNumb']).exists():
                    filteredProfiles.append(each)
                    print(each.user)
                    foundBoth = True
                    continue 
                else: 
                    print("went through else")
                    if each.courses.filter(courseAbbv=request.POST['courseAb']).exists() and not foundBoth:
                        filteredProfiles.append(each)
                    if each.courses.filter(courseNumber=request.POST['courseNumb']).exists() and not foundBoth:
                        filteredProfiles.append(each)

            allProfiles = filteredProfiles

    else:
        allProfiles = Profile.objects.all()
    
    context = {
        'allProfiles' : allProfiles
    }
    return render(request, 'findBuddies.html', context)

def editProfile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    theUser = Profile.objects.get(user_id=request.user.id)

    form = EditProfileForm(request.POST)
    if request.method == 'POST':
        editedProfile = Profile.objects.get(user_id=request.user.id)
        if 'Update' in request.POST:
            if form.is_valid():
                editedProfile.about = form.cleaned_data['about']
                editedProfile.major = form.cleaned_data['major']
                editedProfile.save()
                return HttpResponseRedirect(reverse('profile'))
        else:
            print(request.POST)
            for x in editedProfile.courses.all():
                if(request.POST.get(x.courseAbbv) and request.POST.get(x.courseAbbv) == x.courseNumber):
                    editedProfile.courses.remove(x)
   
    context = {
        'form': form,
        'user': theUser
    }
    return render(request, 'editProfile.html', context)
