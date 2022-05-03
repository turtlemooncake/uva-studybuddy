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
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse

from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=scopes)
#credentials = flow.run_console()
import pickle
#pickle.dump(credentials, open("token.pkl", "wb"))
credentials = pickle.load(open("token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)

result = service.calendarList().list().execute()
result['items'][0]

calendar_id = result['items'][0]['id']
result = service.events().list(calendarId=calendar_id, timeZone="America/New_York").execute()
result['items'][0]

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
    dupUser = False
    form = ProfileForm(request.POST) 
    if Profile.objects.filter(user_id=request.user.id).exists() and request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if (form.is_valid()):
        print(request.POST['user'])
        preferredName = request.POST['user']
        try:
            request.user.username = preferredName
            request.user.save()
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return HttpResponseRedirect(reverse('profile'))

        except:
            dupUser = True

    
    context = {
        'form': form,
        'dupUser': dupUser,
    }
       
    return render(request, 'registerProfile.html', context)


def session(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    invalidDate = False

    if request.method == 'POST':
        form = SessionForm(request.POST)

        # if form.is_valid():
        if 'Send' in request.POST:
            if(request.POST.get('created_date') >= request.POST.get('end_date')):
                invalidDate = True
            else:
                new_session = StudySession()
                #session.users = request.user.objects.values_list('username', flat='True')
                new_session.save()
                #session.users.add(request.POST.get('users'))
                temp = request.POST.getlist('users')
                #session.m2mfield.add(*temp)
                new_session.users.add(*temp)
                #return HttpResponse(request.POST.items())
                new_session.creator = request.user
                new_session.date = request.POST.get('created_date')[0:10]
                new_session.time = request.POST.get('created_date')[11:19]
                new_session.location = request.POST.get('location')
                new_session.subject = request.POST.get('subject')
                new_session.created_date = request.POST.get('created_date')
                new_session.end_date = request.POST.get('end_date')
                new_session.save()

            names = []
            for member in new_session.users.all():
                    names.append(member.username)
            event = {
                'summary': request.POST.get('subject') + " Study Session",
                'location': request.POST.get('location'),
                'description': 'Let\'s work together on this class!',
                'start': {
                    'dateTime': new_session.created_date[0:10] + 'T' + new_session.created_date[11:19] + '-07:00',
                    # 'dateTime': new_session.created_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'dateTime': new_session.end_date[0:10] + 'T' + new_session.end_date[11:19] + '-07:00',
                    # 'dateTime': '2022-05-28T17:00:00-07:00',
                    'timeZone': 'America/New_York',
                },
                # 'attendees': [
                #     {'email': 'lpage@example.com'},
                #     {'email': 'sbrin@example.com'},
                # ],
                'attendees': names,
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            service.events().insert(calendarId=calendar_id, body=event).execute()
            # print('Event created: %s' % (event.get('htmlLink')))
            return HttpResponseRedirect(reverse('my_sessions'))

    else:
        form = SessionForm()

    return render(request, 'newSession.html', {'form': form, 'invalidDate': invalidDate,})

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
            if(s.created_date and s.created_date >= datetime.now().astimezone()):
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
    result = service.calendarList().list().execute()
    result['items'][0]
    calendar_id = result['items'][0]['id']
    result = service.events().list(calendarId=calendar_id,
                                   timeZone="America/New_York").execute()
    result['items'][0]
    return render(request, 'calendar.html')

def addCourses(request):
    if not request.user.is_authenticated or not (Profile.objects.filter(user_id=request.user.id)).exists():
        return HttpResponseRedirect(reverse('login'))
        
    allCourses = Course.objects.all() 
    theUser = Profile.objects.get(user_id=request.user.id)
    courseValid = True
    addedSuccess = False
    dupCourse = False
    validSearch = True

    if request.method == 'POST':
        if 'Filter' in request.POST:
            if Course.objects.filter(courseAbbv=request.POST['courseAb']).exists(): 
                if Course.objects.filter(courseAbbv=request.POST['courseAb'], courseNumber=request.POST['courseNumb']).exists(): 
                    allCourses = Course.objects.filter(courseAbbv=request.POST['courseAb'], courseNumber=request.POST['courseNumb'])
                elif not (request.POST['courseNumb'] == ''):
                    validSearch = False
                else:
                    allCourses = Course.objects.filter(courseAbbv=request.POST['courseAb'])
            else:
                validSearch = False

        elif 'Add Course' in request.POST:    
            if (Course.objects.filter(courseAbbv=request.POST['courseAb'], courseNumber=request.POST['courseNumb']).exists()): 
                if not theUser.courses.filter(courseAbbv=request.POST['courseAb'], courseNumber=request.POST['courseNumb']).exists():
                    theUser.courses.add(Course.objects.get(courseAbbv=request.POST['courseAb'], courseNumber=request.POST['courseNumb']))
                else:
                    dupCourse = True
                courseValid = True
                addedSuccess = True
            else:
                courseValid = False
                addedSuccess = False
                dupCourse = False
        
        elif 'Reset Search' in request.POST:
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
                addedSuccess = False
                dupCourse = False
            
        print('in post expression')
    else:
        allCourses = Course.objects.all()
    
    context = {
        'allCourses' : allCourses,
        'courseValid' : courseValid,
        'addedSuccess' : addedSuccess,
        'dupCourse' : dupCourse,
        'validSearch' : validSearch,
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
