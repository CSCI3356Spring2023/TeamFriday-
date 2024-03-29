from django import forms
import datetime as dt
from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
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
    notifications = models.IntegerField(default=0)
    ##a user can have multiple accounts type
    username = models.CharField(max_length=20,unique=False,default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

# Admin profle model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    department = models.CharField(max_length=20)

    def __str__(self):
        return self.firstname + ' ' + self.lastname

#-- Application data model
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=False)
    related_course = models.ForeignKey('Course', on_delete=models.CASCADE, primary_key=False, related_name='course', default=1, blank=True)
    course_name = models.CharField(
        max_length=60, 
        default='')# ex)CSCI1101.02 = 11 characters
    # In our prototype, this was done as a dropdown, database accessed already
    taken_prev = models.CharField( # Have you taken this course before
        max_length=3,
        choices= [('yes', 'Yes'), ('no', 'No')],
        default= 'No'
    )
    prev_desc = models.CharField(max_length=200, default='test') # Previous experience description
    resume = models.FileField(default='',blank=True, upload_to='resumes/')
    coverl_desc = models.TextField(max_length=1000, default='test')

    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='Available',
    )
    offer_flag = models.BooleanField(default=False)
    
    def __str__(self):
        if self.user.is_student: 
            student = Student.objects.get(user=self.user)
            course = Course.objects.get(id=self.related_course_id)
            self.course_name = course.course_code
            return self.course_name[0:8] + ': ' + student.firstname + ' ' + student.lastname

        return self.course_name[0:8] + ': Test application'

#-- Course data model
class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=False)
    professor = models.CharField(max_length=100)
    department = models.CharField(max_length=4)
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=4)
    section = models.CharField(max_length=1)
    course_code= models.CharField(max_length=60, default='TEST0000.0: default_code')
    applications = models.ManyToManyField(Application, default='', blank=True)
    DAYS_CHOICES = (
		('M', 'M'),
		('T', 'T'),
		('W', 'W'),
		('TH', 'T'),
		('F', 'F'),
	)
    CHOICE = (('yes', 'Yes'),
                 ('no', 'No'))
    HOURS = (('1', '1'),
             ('2', '2'),
             ('3', '3'),
             ('4', '4'),
             ('5', '5'))
    
    days = MultiSelectField(max_length=50, choices=DAYS_CHOICES)
    disc_flag = models.CharField(max_length=3, choices= CHOICE, default='no')
    disc_section = models.CharField(max_length=30, blank=True)  # Make a new table?
    start_time = models.TimeField(default=dt.time(00, 00))
    end_time = models.TimeField()
    positions = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
     )
    filled = models.IntegerField(default='0')
    graded_hw = models.CharField(max_length=3, choices= CHOICE, default='no')
    office_hours = models.CharField(max_length=1, choices=HOURS, default='2')
    desc = models.TextField(max_length=2000)
    open = models.BooleanField(default=True)
    
    def __str__(self):
	    return str(self.course_code)  

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
    applications = models.ManyToManyField(Application, default='', blank=True)

    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Pending', 'Pending'),
        ('Hired', 'Hired'),
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='available',
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
    course_list = models.ManyToManyField(Course, default='', blank=True)

    def __str__(self):
        return self.firstname + ' ' + self.lastname

class Semester(models.Model):
    SESSIONS = (('SPRING', 'SPRING'),
                ('SUMMER', 'SUMMER'),
                ('FALL', 'FALL'),
                )
    session = models.CharField(max_length=6, choices=SESSIONS, default='SPRING')
    year = models.CharField(max_length=2, default='23')
    STATUS_CHOICES = (
        ('closed', 'Closed'),
        ('open', 'Open'),
    )
    current = models.BooleanField(default=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES)
    total_positions = models.IntegerField(default=10)
    total_filled = models.IntegerField(default=0)
    # add many to many fields later?

    def __str__(self):
        return self.session + '-' + self.year


class Notification(models.Model):
    STATE_CHOICES = (
        ('offer sent', 'Offer Sent'),
        ('rejected', 'Rejected'),
        ('accepted offer', 'Accepted Offer'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=False)
    timestamp = models.TimeField(auto_now_add=True)
    message = models.TextField(max_length=2000)
    seen = models.BooleanField(default=False)
