from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.


## Creating custom user class
# Have three boolean fields, is_student, is_instructor, is_admin
# Class User(AbstractUser):
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(defalse=False)
    email = models.EmailField(('Email Address'), unique=True)

    ##a user can have multiple accounts type
    username = models.CharField(max_length=20,unique=False,default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

# Student profile model
# all info related to a student from d3 pdf.
# Class Student(models.model):
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    major = models.CharField(max_length=20)
    eagle_id = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,8}$')])
    available = models.BooleanField(default=True)
    graduation_year = models.CharField(max_length = 4,)
    def __str__(self):
        return self.firstname
## Instructor profile model:
# Class Instructor(models.model):
#.......
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    position = models.CharField(max_length=30)

    def __str__(self):
        return self.firstname



## Course data model
#create fields for all relevant course info

# Class Course(models.model):
#.....


## Application data model
# create fields for all relevant application info

class Application(models.model):

    course = models.CharField(max_length=12) # ex)CSCI1101.02 = 11 characters
    experience = models.BooleanField(default=False) # Have you taken this course before?
    professor = models.CharField(max_length=25) # Name of the Professor when you took it (otherwise, N/A.)
    semester = models.CharField(max_length=12) # Semester you took the course (otherwise, N/A.)
    #resume = #file upload
    cover_letter = models.CharField(max_length=400) # I want to write a function that checks 400 words, not 400 characters!
