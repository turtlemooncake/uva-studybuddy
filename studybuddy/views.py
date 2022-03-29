from http.client import HTTPResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Profile

def login(request):
    if (request.user.is_authenticated):
        return render(request, 'profile.html')
    return render(request, 'index.html')

