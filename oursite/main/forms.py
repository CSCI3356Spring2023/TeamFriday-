from django import forms
from django.db import models
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User, Student, Instructor, Admin, Course

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=20)
    file = forms.FileField()

class StudentSignUpForm(UserCreationForm):
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
    firstname = forms.CharField()
    lastname = forms.CharField()
    email = forms.EmailField()
    major = forms.CharField()
    grade = forms.ChoiceField(choices=YEAR_IN_SCHOOL_CHOICES)
    eagle_id = forms.CharField()

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'email', 'major', 'grade', 'eagle_id')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        user.is_student = True
        user.email = email
        user.save()
        Student.objects.create(
            user=user,
            firstname=self.cleaned_data.get('firstname'),
            lastname=self.cleaned_data.get('lastname'),
            email=email,
            major=self.cleaned_data.get('major'),
            grade=self.cleaned_data.get('grade'),
            eagle_id=self.cleaned_data.get('eagle_id')
        )
        return user
    
class InstructorSignUpForm(UserCreationForm):
    firstname = forms.CharField()
    lastname = forms.CharField()
    position = forms.CharField()
    email = forms.EmailField()

    class Meta: 
        model = User
        fields = ('firstname', 'lastname', 'position', 'email')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        user.is_instructor = True
        user.email = email
        user.save()
        Instructor.objects.create(
        user=user,
        firstname=self.cleaned_data.get('firstname'),
        lastname=self.cleaned_data.get('lastname'),
        position=self.cleaned_data.get('position'),
        email=email,
    )
        return user
class AdminSignUpForm(UserCreationForm):
    firstname = forms.CharField()
    lastname = forms.CharField()
    department = forms.CharField()
    email = forms.EmailField()

    class Meta: 
        model = User
        fields = ('firstname', 'lastname', 'department', 'email')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        user.is_admin = True
        user.is_staff = True
        user.email = email
        user.save()
        Admin.objects.create(
            user=user,
            firstname=self.cleaned_data.get('firstname'),
            lastname=self.cleaned_data.get('lastname'),
            department=self.cleaned_data.get('department'),
            email=email,
        )
        return user

class addCourseForm(forms.Form):
    courseName = forms.CharField(label='Course Name')
    courseNumber = forms.CharField(label='Course Number', max_length=8)
    courseSection = forms.CharField(label='Course Section',max_length=2)
    startTime = forms.TimeField(label='Start time') 
    endTime = forms.TimeField(label='End time')
    date = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=Course.DAYS_CHOICES, label='Days of course')
    discussionBool = forms.BooleanField(required=False,label='Does this course have a discussion section?')
    discussionSection = forms.CharField(max_length=12,required=False,label='Discussion section') # dropdown
    officeHours = forms.CharField(max_length=2,label='Required office hours per week') #dropdown?
    gradedInOfficeHrs = forms.BooleanField(label='Homework/assignments graded in meetings?')
