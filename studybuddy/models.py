from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=300)
    major = models.CharField(max_length=50)
    courses = models.ManyToManyField('Course', blank=True)
    # picture = models.TextField(blank=True, null=True, default="https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg")

class StudySession(models.Model):
    users = models.ManyToManyField(User)
    #date = models.DateField()
    time = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    subject = models.CharField(max_length=10)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="creator_of_session")
    created_date = models.DateTimeField('date created', default=timezone.now, blank=True, null=True)
    end_date = models.DateTimeField('date created', default=timezone.now, blank=True, null=True)

class MessageTwo(models.Model):
    to = models.ManyToManyField(User)
    sent_by = models.CharField(max_length=100, default='')
    message = models.CharField(max_length=100)
    created_date = models.DateTimeField('date created', default=timezone.now, blank=True, null=True)

class Course(models.Model):
    courseAbbv = models.CharField(max_length=5, default='')
    courseNumber = models.CharField(max_length=5, default='')
    courseTitle = models.CharField(max_length=120, null=True, default='')
    courseTopic = models.CharField(max_length=120, null=True, default='')

    def __str__(self):
        return self.courseAbbv

