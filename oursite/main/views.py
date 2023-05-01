from django.shortcuts import render, redirect
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, CreateView, DetailView
from django.core.exceptions import ObjectDoesNotExist
import os

from .forms import addCourseForm, StudentSignUpForm, InstructorSignUpForm, AdminSignUpForm, CreateApplicationForm
from .models import User, Student, Instructor, Admin, Course, Application, Semester, Notification

from django.core.mail import send_mail

#--Authentication
class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

#	email = self.request.user.email
#        send_mail(
#                'Subject: Successfully Created Student User',
#                'You have successfully registered as a student. Thanks for using EagleHire!',
#                'BCEagleHire@gmail.com',
#                [email],
#                fail_silently=False,
#        )	

        return redirect('/home')

class InstructorSignUpView(CreateView):
    model = User
    form_class = InstructorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'instructor'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

#	email = self.request.user.email
#        send_mail(
#                'Subject: Successfully Created Instructor User',
#                'You have successfully registered as an instructor. Thanks for using EagleHire!',
#                'BCEagleHire@gmail.com',
#                [email],
#                fail_silently=False,
#        )

        return redirect('/home')

class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
	
#	email = self.request.user.email
#        send_mail(
#                'Subject: Successfully Created Admin User',
#                'You have successfully registered as an admin. Thanks for using EagleHire!',
#                'BCEagleHire@gmail.com',
#                [email],
#                fail_silently=False,
#        )	

        return redirect('/home')
    

#--Web pages
@login_required()
def home(response):
    return render(response, 'main/home.html', {})

@login_required
def course_list(request):
    template_name = 'main/home.html'
    courses = Course.objects.all()
    try: 
        semester = Semester.objects.get(current=True)
    except ObjectDoesNotExist:
        semester = None 
        return semester_error(request, semester)
    if semester.status == 'closed' or semester.total_positions == semester.total_filled: 
        return semester_error(request, semester)
    
    return render(request, template_name, {'courses': courses} )

def semester_error(request, semester):
    template_name = 'main/semester_error.html'
    return render(request, template_name, {"semester": semester})

class app_error(ListView):
    model = Course
    template_name = 'main/application_error.html'
    context_object_name = 'courses'

def fp(response):
    if response.user.is_authenticated:
        return redirect('/home')

    return render(response, 'main/fp.html', {})

class addCourse(CreateView):
    model = Course
    form_class = addCourseForm
    template_name = 'main/addcourse.html'

    def get_context_data(self, **kwargs):
        kwargs['form_type'] = 'course'
        return super().get_context_data(**kwargs)

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        course_code = self.object.department + self.object.number + ': ' + self.object.name
        self.object.course_code = course_code
        self.object.save()

        email = self.request.user.email
        send_mail(
            'Successfully Created Course',
            'Your course has been successfully registered. Thanks for using EagleHire!',
            'BCEagleHire@gmail.com',
            [email],
            fail_silently=False
	)
		
        return redirect('/home')

class CreateApplication(CreateView):
    model = Application
    form_class = CreateApplicationForm
    template_name = 'main/create_app.html'

    def get_context_data(self, **kwargs):
        kwargs['form_type'] = 'application'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

	# email
        email = self.request.user.email
        send_mail(
                'Subject: Successfully Created Application',
                'Your application has been successfully created. Thanks for using EagleHire!',
                'BCEagleHire@gmail.com',
                [email],
                fail_silently=False,
        )

        return redirect('/home')

def apply(response, id):
    if response.method == "POST":
        form = CreateApplicationForm(response.POST, response.FILES)
        user = response.user
        if user.is_student: student = Student.objects.get(user=user)
        course = Course.objects.get(id=id)
        apps = Application.objects.filter(user=user)
        app_count = len(apps)

        if form.is_valid() and app_count < 5:
            application = Application(course_name = course.course_code, user=user)
            resume = response.FILES['resume']
            application.resume = resume
            application.save()
            course.applications.add(application)
            course.save()
            if user.is_student: 
                student.applications.add(application)
                student.save()

#	email = self.request.user.email
#        send_mail(
#                'Subject: Successfully Applied',
#                'You have successfully applied to a course. Thanks for using EagleHire!',
#                'BCEagleHire@gmail.com',
#                [email],
#                fail_silently=False,
#        )
        else:
            return redirect('/apply/error/')
        return redirect('/applications')
    else:
            form = CreateApplicationForm()

    return render(response, "main/create_app.html",{'form':form})   

def InstructorSummaryView(response):
    context = {}
    if response.method == "GET" :
        courses = Course.objects.filter(user = response.user)
        apps = []
        for course in courses:
            apps.extend(course.applications.all())
        for app in apps:
            if app.user.is_student:
                student = Student.objects.get(user=app.user)
                if student.status == 'Hired': 
                    if app.offer_flag: app.status = 'Accepted'
                    else: app.status = 'Unavailable'
                elif student.status == 'Pending': app.status = 'Pending'
                elif student.status == 'Available' and app.status != 'Rejected': app.status = 'Available'
                app.save()
        context['applications'] = apps
        context['courses'] = courses
    return render(response, "main/Instructor_Summary.html",context)

def student_apps(response):
    context = {}

    if response.method == "GET":
        user = response.user
        student = Student.objects.get(user=user)
        apps = student.applications.all()
        for app in apps:
            if app.user.is_student:
                student = Student.objects.get(user=app.user)
                if student.status == 'Hired': 
                    if app.offer_flag: app.status = 'Accepted'
                    else: app.status = 'Unavailable'
                elif student.status == 'Pending': app.status = 'Pending'
                elif student.status == 'Available' and app.status != 'Rejected': app.status = 'Available'
                app.save()
        context['applications'] = apps
    return render(response, "main/student_apps.html",context)

class ApplicationDetail(DetailView):
    model = Application
    template_name = 'main/app_detail.html'

def show_pdf(request, pk):
    application = Application.objects.get(id=pk)
    resume = application.resume
    return FileResponse(open(resume.path, 'rb'), content_type='application/pdf')
def notification_list(response):
    context = {}

    if response.method == "GET":
        user = response.user
        notifications = Notification.objects.filter(user=user)

        context['notifications'] = notifications

    
    return render(response, "main/notifications.html", context)


def accept_offer(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    student = application.user
    course = application.related_course
    student.status = 'Hired'
    application.status = 'Accepted'
    course.filled += 1

def reject_offer(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    student = application.user
    
    student.save()
    application.save()

    return redirect('/instructor_summary')



def sendOffer(response, pk):
    application = Application.objects.get(id=pk)
    student = Student.objects.get(user=application.user) 
    student.status = 'Pending'
    application.offer_flag = True
    application.save()
    student.save()

    course = application.related_course
    msg = "Your application for " + str(course) + " has been reviewed and professor " + course.professor + " has sent you an offer!"
    notification = Notification(user=application.user, message=msg)
    notification.save()

    return redirect('/instructor_summary')


def rejectApp(response, pk):
    application = Application.objects.get(id=pk)
    student = Student.objects.get(user=application.user) 
    student.status = 'Available'
    application.status = 'Rejected'
    application.save()
    student.save()

    course = application.related_course
    msg = "Your application for " + str(course) + " has been rejected."
    notification = Notification(user=application.user, message=msg)
    notification.save()

    return redirect('/instructor_summary')



   


