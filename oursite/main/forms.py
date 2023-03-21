from django import forms
from django.db import models
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User, Student


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=20)
    file = forms.FileField()

# class StudentSignUpForm(UserCreationForm):
#...



# class InstructorSignUpForm(UserCreationForm):
# ...



# class SignUpForm(UserCreationForm):
# ...



class addCourseForm(forms.Form):
    courseName = forms.TextField()
    courseNumber = forms.CharField(label="Number", max_length=8)
    courseSection = forms.CharField(label="Section",max_length=2)
    startTime = forms.TimeField() 
    endTime = forms.TimeField()
    date = forms.CharField(         #hopefully selecting from list
        max_length=8,
        widget=forms.Select(choices=DATE_CHOICES),
    )
    discussionBool = forms.BooleanField(required=False)
    discussionSection = forms.CharField(max_length=12,required=False) # dropdown
    officeHours = forms.CharField(max_length=2) #dropdown?
    gradedInOfficeHrs = forms.BooleanField()
