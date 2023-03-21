from django.db import models
from django import forms
from multiselectfield import MultiSelectField

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from multiselectfield import MultiSelectField
# Create your models here.


## Creating custom user class
# Have three boolean fields, is_student, is_instructor, is_admin
# Class User(AbstractUser):
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
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
        return self.firstname + ' ' + self.lastname

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
        return self.firstname + ' ' + self.lastname

# Admin profle model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    department = models.CharField(max_length=20)

    def __str__(self):
        return self.firstname + ' ' + self.lastname


## Course data model
#create fields for all relevant course info

class Course(models.Model):

	courseNumber = models.CharField(max_length=8)
	courseName = models.CharField(max_length=100)
	courseDescription = models.TextField()
	courseSection = models.PositiveIntegerField()
	courseInstructor = models.CharField(max_length=100)

	DAYS_CHOICES = (
		('M', 'Monday'),
		('T', 'Tuesday'),
		('W', 'Wednesday'),
		('TH', 'Thursday'),
		('F', 'Friday'),
	)

	courseDate = MultiSelectField(max_length=50, choices=DAYS_CHOICES)

	courseStartTime = models.TimeField()
	courseEndTime = models.TimeField()
	courseTANeeded = models.IntegerField()

	courseMarkHW = models.BooleanField(default=False)
	courseOfficeHours = models.PositiveIntegerField()

	def __str__(self):
		return self.firstname + ' ' + self.lastname

## Application data model
class Application(models.Model):

    def word_counter(string):
        return string.count(" ") + 1

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    course = models.CharField(max_length=12) # ex)CSCI1101.02 = 11 characters
    # In our prototype, this was done as a dropdown, database accessed already

    experience = models.BooleanField(default=False) # Have you taken this course before?
    professor = models.CharField(max_length=25) # Name of the Professor when you took it (otherwise, N/A.)
    semester = models.CharField(max_length=12) # Semester you took the course (otherwise, N/A.)
    #resume = #file upload
    #cover_letter = models.CharField(max_length=(word_counter())>=400) # I want to write a function that checks 400 words, not 400 characters!

    def __str__(self):
        return self.firstname + ' ' + self.lastname



class addCourse(models.Model):

    DATE_CHOICES = (('MONDAY','Monday'),
    ('TUESDAY','Tuesday'),
    ('WEDNESDAY','Wednesday'),
    ('THURSDAY','Thursday'),
    ('FRIDAY','Friday'),
    ('M/W/F','m/w/f'),
    ('M/W','m/w'),
    ('T/TH','t/th'),


# class addCourse(models.Model):
#     # fields of the model
#     courseName = models.TextField()
#     courseNumber = models.CharField(max_length=8)
#     courseSection = models.CharField(max_length=2)
#     startTime = models.TimeField()
#     endTime = models.TimeField()
#     # want to select from a list but idk how to do that lol
#     date = models.CharField(max_length=10,choices=DATE_CHOICES) # idk how to do list so rn format is like type M/W/F or T/TH
#     discussionBool = models.BooleanField()
#     discussionSection = models.CharField(max_length=12) # dropdown
#     officeHours = models.CharField(max_length=2) #dropdown?
#     gradedInOfficeHrs = models.BooleanField()

#         # renames the instances of the model
#         # with their title name
#     def __str__(self):
#         return self.firstname + ' ' + self.lastname
