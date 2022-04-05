from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=300); 
    major = models.CharField(max_length=50); 
    courses = models.ManyToManyField('Course', blank=True)


class Course(models.Model):
    courseAbbv = models.CharField(max_length=5, default='')
    courseNumber = models.CharField(max_length=5, default='')
    courseTitle = models.CharField(max_length=120, null=True, default='')
    courseTopic = models.CharField(max_length=120, null=True, default='')

    def __str__(self):
        return self.courseAbbv

# class Event(models.Model):
#     date = models.DateField()
#     partners = models.ManyToManyField('User', blank=True)