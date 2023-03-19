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