from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=300)
    major = models.CharField(max_length=50)
    courses = models.ManyToManyField('Course', blank=True)

class StudySession(models.Model):
    users = models.ManyToManyField(User)
    #date = models.DateField()
    time = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    subject = models.CharField(max_length=10)

class Message(models.Model):
    to = models.ManyToManyField(User)
    sent_by = models.CharField(max_length=100)
    message = models.CharField(max_length=100)

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

