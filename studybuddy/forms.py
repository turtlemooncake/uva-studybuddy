from django.forms import ModelForm
from .models import Profile
from .models import StudySession, MessageTwo
from django import forms

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'major']

class SessionForm(ModelForm):
    class Meta:
        model = StudySession
        fields = ['users', 'date', 'time', 'location', 'subject', 'created_date', 'end_date']

class MessageForm(ModelForm):
    class Meta:
        model = MessageTwo
        fields = ['to', 'message']

class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'major']

    # class Meta:
    #     model = Profile
    #     fields = ['about', 'major']

# class EventForm(ModelForm):
#     class Meta:
#         model = 
