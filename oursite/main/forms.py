from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from register.models import User, Student


# class StudentSignUpForm(UserCreationForm):
#...



# class InstructorSignUpForm(UserCreationForm):
# ...



# class SignUpForm(UserCreationForm):
# ...


class addCourse(forms.Form):
    courseName = models.TextField()
    courseNumber = models.CharField(label="Number", max_length=8,required=True)
    courseSection = models.CharField(label="Section",max_length=2,required=True)
    startTime = models.TimeField(required=True) 
    endTime = models.TimeField(required=True)
    # want to select from a list but idk how to do that lol 
    date = models.CharField(max_length=8, required=True) # idk how to do list so rn format is like type M/W/F or T/TH
    discussionBool = models.BooleanField(required=False)
    discussionSection = models.CharField(max_length=12,required=False) # dropdown
    officeHours = models.CharField(max_length=2,required=True) #dropdown?
    gradedInOfficeHrs = models.BooleanField(required=True)
