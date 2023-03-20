from django.db import models

# Create your models here.


## Creating custom user class
# Have three boolean fields, is_student, is_instructor, is_admin
# Class User(AbstractUser):
#.....


# Student profile model
# all info related to a student from d3 pdf.
# Class Student(models.model):
# .......
#  ....
# ....


## Instructor profile model:
# Class Instructor(models.model):
#.......



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
