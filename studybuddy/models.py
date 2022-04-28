from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="creator_of_session")
    created_date = models.DateTimeField('date created', default=timezone.now, blank=True, null=True)
    
class MessageTwo(models.Model):
    to = models.ManyToManyField(User)
    sent_by = models.CharField(max_length=100, default='')
    message = models.CharField(max_length=100)
    created_date = models.DateTimeField('date created', default=timezone.now, blank=True, null=True)

class MessageTwo(models.Model):
    to = models.ManyToManyField(User)
    sent_by = models.CharField(max_length=100, default='')
    message = models.CharField(max_length=100)

class Course(models.Model):
    courseAbbv = models.CharField(max_length=5, default='')
    courseNumber = models.CharField(max_length=5, default='')
    courseTitle = models.CharField(max_length=120, null=True, default='')
    courseTopic = models.CharField(max_length=120, null=True, default='')

    def __str__(self):
        return self.courseAbbv

class Room(models.Model):
    """Represents chat rooms that users can join"""
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    slug = models.CharField(max_length=50)

    def __str__(self):
        """Returns human-readable representation of the model instance."""
        return self.name

# class Event(models.Model):
#     date = models.DateField()
#     partners = models.ManyToManyField('User', blank=True)

