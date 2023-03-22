from django import forms


# Create your models here.

from django.db import models
from django.conf import settings
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
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    major = models.CharField(max_length=20)
    eagle_id = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,8}$')])
    available = models.BooleanField(default=True)
    grade = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    courseNumber = models.CharField(max_length=8)
    courseName = models.CharField(max_length=100)
    courseSection = models.PositiveIntegerField()
    courseInstructor = models.CharField(max_length=100)

    DAYS_CHOICES = (
		('M', 'Monday'),
		('T', 'Tuesday'),
		('W', 'Wednesday'),
		('TH', 'Thursday'),
		('F', 'Friday'),
	)
    HOURS = (('1', '1'),
             ('2', '2'),
             ('3', '3'),
             ('4', '4'),
             ('5', '5'))
    courseDate = MultiSelectField(max_length=50, choices=DAYS_CHOICES)

    courseStartTime = models.TimeField()
    courseEndTime = models.TimeField()
    courseTANeeded = models.CharField(max_length=1, choices=HOURS, default='2')

    courseMarkHW = models.BooleanField(default=False)
    courseOfficeHours = models.CharField(max_length=1, choices=HOURS, default='2')
    courseDescription = models.CharField(max_length=200)
    def __str__(self):
	    return self.firstname + ' ' + self.lastname

## Application data model
class Application(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    CSCI1101_01 = 'CS1 Section 1'
    CSCI1101_02 ='CS1 Section 2'
    COURSE_CHOICES = [
        (CSCI1101_01, 'CS1 Section 1'),
        (CSCI1101_02, 'CS1 Section 2')
    ]
    
    course = models.CharField(
        max_length=20,
        choices=COURSE_CHOICES,
        default=CSCI1101_01,) # ex)CSCI1101.02 = 11 characters
    # In our prototype, this was done as a dropdown, database accessed already
    taken_prev = models.CharField( # Have you taken this course before
        max_length=3,
        choices= [('yes', 'Yes'), ('no', 'No')],
        default= 'No'
    )
    prev_desc = models.CharField(max_length=200, default='test') # Previous experience description
    #resume = #file upload
    coverl_desc = models.TextField(max_length=1000, default='test')

    def __str__(self):
        return self.firstname + ' ' + self.lastname

