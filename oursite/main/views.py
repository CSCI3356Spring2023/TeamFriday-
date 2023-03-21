from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login/')
def home(response):
    return render(response, 'main/home.html', {})

def fp(response):
    return render(response, 'main/frontpage.html', {})
# StudentSignupView

# CreateCourseView

# CreateApplicationView

# InstructorSignupView


