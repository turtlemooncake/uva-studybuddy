from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=300); 
    major = models.CharField(max_length=50); 