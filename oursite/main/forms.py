from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from register.models import User, Student


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=20)
    file = forms.FileField()

# class StudentSignUpForm(UserCreationForm):
#...



# class InstructorSignUpForm(UserCreationForm):
# ...



# class SignUpForm(UserCreationForm):
# ...