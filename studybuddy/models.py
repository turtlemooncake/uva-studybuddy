from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=300); 
    major = models.CharField(max_length=50); 


class Course(models.Model):
    dep = models.CharField(max_length=5, blank = True, null = True)
    number = models.CharField(max_length=4, blank = True, null = True)
    courseTitle = str(dep) + " " + str(number)