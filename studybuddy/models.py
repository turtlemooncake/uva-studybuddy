from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=300); 
    major = models.CharField(max_length=50);

class StudySession(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    time = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
