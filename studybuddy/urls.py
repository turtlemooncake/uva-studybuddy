"""studybuddy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path as url
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('register/', views.register, name='register'),
    path('', views.login, name='login'), #EDIT PATHS TO TEMPLATES LATER
    path('home/', views.home, name="home"),
    path('aboutus/', views.aboutUs, name="aboutUs"),
    path('studysession/', views.session, name="session"),
    path('mysessions/', views.my_sessions, name="my_sessions"),
    path('sendmessage/', views.send_message, name="send_message"),
    path('mymessages/', views.my_messages, name="my_messages"),
    path('profile/', views.profile, name="profile"),
    path('calendar/', views.calendar, name="calendar"),
    path('findBuddies/', views.findBuddies, name="buddies"),
    path('addCourses/', views.addCourses, name="addCourses"),
    path('logout/', views.logOut, name="logout"),
    path('editProfile/', views.editProfile, name="editProfile"),
    path('chat/', views.all_rooms, name="allrooms"),
    #path(r'rooms/(?P<slug>[-\w]+)/$', views.room_detail, name="room_detail"),
    path('chat/<str:slug>/', views.room_detail, name="room_detail"),
    url(r'token$', views.token, name="token"), 
]

urlpatterns += staticfiles_urlpatterns()