from django import forms
from django.db import models
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
import datetime as dt

from .models import User, Student, Instructor, Admin, Course, Application

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
        user.is_teacher = True
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
        user.is_superuser = True
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

class addCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(addCourseForm, self).__init__(*args, **kwargs)
    HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
    DEPT = (('CSCI', 'CSCI'),
            ('MATH', 'Mathematics'),
            ('BIOL', 'Biology'),
            ('PHYS', 'Physics'))
    DAYS = (('M', 'Monday'),
            ('T', 'Tuesday',),
            ('W', 'Wednsday'),
            ('TH', 'Thursday'),
            ('F', 'Friday'))
    CHOICE = (('yes', 'Yes'),
                 ('no', 'No'))
    HOURS = (('1', '1'),
             ('2', '2'),
             ('3', '3'),
             ('4', '4'),
             ('5', '5'))
    department = forms.ChoiceField(label='Select department:', choices=DEPT)
    name = forms.CharField(label='Course Name')
    number = forms.CharField(label='Course Number (e.g. 1011)', max_length=4)
    section = forms.ChoiceField(label='Course Section', choices=HOURS)
    instructor = forms.CharField(label='Course Instructor (Last name)')
    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=DAYS, label='Days')
    start_time = forms.TimeField(label='Start time', widget=forms.Select(choices=HOUR_CHOICES)) 
    end_time = forms.TimeField(label='End time', widget=forms.Select(choices=HOUR_CHOICES))
    disc_flag= forms.ChoiceField(label='Does the course have discussion sections? ', choices=CHOICE)
    disc_section= forms.CharField(max_length=12,required=False,label='Discussion section')  # make a new table for discussion sections?
    office_hours = forms.ChoiceField(label= 'Required office hours per week', choices=HOURS) 
    graded_hw = forms.ChoiceField(label='Homework/assignments graded in meetings?', choices=CHOICE )
    positions = forms.ChoiceField(label='Number of TAs needed', choices=HOURS)
    desc = forms.CharField(label='Description of the course', widget=forms.Textarea)

    class Meta:
        model = Course
        fields = ('department', 'name', 'number', 'section', 'instructor', 'days', 'start_time', 'end_time', 'disc_flag', 'disc_section', 'office_hours', 'graded_hw', 'positions', 'desc')


class CreateApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateApplicationForm, self).__init__(*args, **kwargs)
    CSCI1101_01 = 'CS1 Section 1'
    CSCI1101_02 ='CS1 Section 2'
    COURSE_CHOICES = [
        (CSCI1101_01, 'CS1 Section 1'),
        (CSCI1101_02, 'CS1 Section 2')
    ]

    course = forms.ChoiceField(label="Please select the course you're applying to", choices=COURSE_CHOICES)
    taken_prev = forms.ChoiceField(label='Have you taken this course before?', choices= (('yes', 'Yes'), ('no', 'No')))
    prev_desc = forms.CharField(
        label='Please state the professor and the semester you took this course. Otherwise N/A',
        widget=forms.Textarea,
        )
    resume = forms.FileField(label="Please upload your resume")
    coverl_desc = forms.CharField(
        label='Use this space to write a cover letter/description',
        widget=forms.Textarea)
    
    class Meta:
        model = Application
        fields = ('course', 'taken_prev', 'prev_desc', 'coverl_desc')
    
