from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from models import User, Student, Instructor, Admin


class StudentSignUpForm(UserCreationForm):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    Year_In_School_Choices = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    ]
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    major = forms.CharField()
    minor = forms.CharField()
    year = forms.ChoiceField(choices = Year_In_School_Choices)
    eagle_id = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'major', 'minor', 'year', 'eagle_id')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        user.is_student = True
        user.email = email
        user.save()
        Student.objects.create(
        user=user,
        first_name=self.cleaned_data.get('first_name'),
        last_name=self.cleaned_data.get('last_name'),
        email=email,
        major=self.cleaned_data.get('major'),
        minor=self.cleaned_data.get('minor'),
        year=self.cleaned_data.get('year'),
        eagle_id=self.cleaned_data.get('eagle_id')
    )
        return user
    
class InstructorSignUpForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    department = forms.CharField()
    email = forms.EmailField()
    eagle_id = forms.CharField()

    class Meta: 
        model = User
        fields = ('first_name', 'last_name', 'department', 'email', 'eagle_id')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        user.is_instructor = True
        user.email = email
        user.save()
        Instructor.objects.create(
        user=user,
        first_name=self.cleaned_data.get('first_name'),
        last_name=self.cleaned_data.get('last_name'),
        department=self.cleaned_data.get('department'),
        email=email,
        eagle_id=self.cleaned_data.get('eagle_id')
    )
        return user
class AdminSignUpForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    department = forms.CharField()
    email = forms.EmailField()
    eagle_id = forms.CharField()

    class Meta: 
        model = User
        fields = ('first_name', 'last_name', 'department', 'email', 'eagle_id')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        user.is_admin = True
        user.email = email
        user.save()
        Admin.objects.create(
        user=user,
        first_name=self.cleaned_data.get('first_name'),
        last_name=self.cleaned_data.get('last_name'),
        department=self.cleaned_data.get('department'),
        email=email,
        eagle_id=self.cleaned_data.get('eagle_id')
    )
        return user