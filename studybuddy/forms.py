from django.forms import ModelForm
from .models import Profile
from .models import StudySession

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'major']

class SessionForm(ModelForm):
    class Meta:
        model = StudySession
        fields = ['users', 'date', 'time', 'location', 'subject']
        #widgets = {'date': forms.DateInput()}
# class EventForm(ModelForm):
#     class Meta:
#         model = 
