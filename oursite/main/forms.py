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
    courseName = forms.charField(label='Course Name')
    courseNumber = forms.CharField(label='Course Number', max_length=8)
    courseSection = forms.CharField(label='Course Section',max_length=2)
    startTime = forms.TimeField(label='Start time') 
    endTime = forms.TimeField(label='End time')
    date = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=DAYS, label='Days of course')
    discussionBool = forms.BooleanField(required=False,label='Does this course have a discussion section?')
    discussionSection = forms.CharField(max_length=12,required=False,label='Discussion section') # dropdown
    officeHours = forms.CharField(max_length=2,label='Required office hours per week') #dropdown?
    gradedInOfficeHrs = forms.BooleanField(label='Homework/assignments graded in meetings?')
