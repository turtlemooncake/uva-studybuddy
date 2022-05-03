from django.forms import ModelForm
from .models import Profile
from .models import StudySession, MessageTwo
from django import forms
from crispy_forms.helper import FormHelper

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
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 

class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'major']
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_show_labels = False 
        self.fields['about'].label = "300 character limit!"
        self.fields['major'].label = False
    # class Meta:
    #     model = Profile
    #     fields = ['about', 'major']

# class EventForm(ModelForm):
#     class Meta:
#         model = 
