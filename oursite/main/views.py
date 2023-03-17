from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

# Create your views here.
def home(response):

    # New branch who dis?


    return render(response, 'main/home.html', {})


#Changes