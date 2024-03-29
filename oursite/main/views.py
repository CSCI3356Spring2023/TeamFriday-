from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, CreateView, DetailView, UpdateView
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
    user = request.user
    getNotifications(user)
    for course in courses:
        if course.filled == course.positions:
            course.open = False
            course.save()
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
    
class EditCourse(UpdateView):
    model = Course
    fields = ('department', 'name', 'number', 'section', 'days', 'start_time', 'end_time', 'disc_flag', 'disc_section', 'office_hours', 'graded_hw', 'positions', 'desc')

    success_url = "/home"


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
            application.taken_prev = response.POST['taken_prev']
            application.prev_desc = response.POST['prev_desc']
            application.coverl_desc = response.POST['coverl_desc']
            application.save()
            course.applications.add(application)
            course.save()
            if user.is_student: 
                student.applications.add(application)
                student.save()

            # Notification
            msg = str(user) + " has applied for the TA position for the " + str(course) + " course!"
            professor = course.user
            notification = Notification(user=professor, message=msg)
            notification.save()

            #Email
            email = response.user.email
            msg =  "You have successfully applied to a TA position for the course: " + str(course) + ". Thanks for using EagleHire!"
            send_mail(
                    'EagleHire: Successfully Applied',
                    msg,
                    'BCEagleHire@gmail.com',
                    [email],
                    fail_silently=False,
            )
        else:
            return redirect('/apply/error/')
        return redirect('/applications')
    else:
            form = CreateApplicationForm()

    return render(response, "main/create_app.html",{'form':form})   

def InstructorSummaryView(response):
    context = {}
    getNotifications(response.user)
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
    getNotifications(response.user)
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
    getNotifications(response.user)
    if response.method == "GET":
        user = response.user
        notifications = Notification.objects.filter(user=user)

        context['notifications'] = notifications

    
    return render(response, "main/notifications.html", context)


def accept_offer(request, id):
    application = get_object_or_404(Application, id=id)
    student = get_object_or_404(Student, user=application.user)
    semester = get_object_or_404(Semester, current=True)
    course = application.related_course
    student.status = 'Hired'
    application.status = 'Accepted'
    course.filled += 1
    semester.total_filled += 1
    
    student.save()
    course.save()
    application.save()
    semester.save()

    course = application.related_course
    msg = str(student) + " has accepted your offer for the " + str(course) + " TA position!"
    professor = get_object_or_404(User, id=course.id)
    notification = Notification(user=professor, message=msg)
    notification.save()

    email = professor.email
    send_mail(
                'EagleHire: Offer accepted',
                msg,
                'BCEagleHire@gmail.com',
                [email],
                fail_silently=False,
            )




    return redirect('/applications')

def reject_offer(request, id):
    application = get_object_or_404(Application, id=id)
    student = get_object_or_404(Student, user=application.user)

    student.status = 'Available'
    application.status = 'Rejected'
    student.save()
    application.save()


    course = application.related_course
    msg = str(student) + " has rejected your offer for the " + str(course) + " TA position!"
    professor = get_object_or_404(User, id=course.id)
    notification = Notification(user=professor, message=msg)
    notification.save()


    email = professor.email
    send_mail(
                'EagleHire: Offer rejected',
                msg,
                'BCEagleHire@gmail.com',
                [email],
                fail_silently=False,
            )

    return redirect('/applications')



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

    email = application.user.email
    send_mail(
                'EagleHire: Offer received',
                msg,
                'BCEagleHire@gmail.com',
                [email],
                fail_silently=False,
            )

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

    email = application.user.email
    send_mail(
                'EagleHire: Application rejected',
                msg,
                'BCEagleHire@gmail.com',
                [email],
                fail_silently=False,
            )

    return redirect('/instructor_summary')


def getNotifications(user):
    try:
        notifications = Notification.objects.filter(user=user)
        total = 0
        for n in notifications:
            if n.seen == False:
                total += 1
        user.notifications = total
    except ObjectDoesNotExist:
        user.notifications = 0

    return True

def seen(response, id):
    notification = get_object_or_404(Notification, id=id)
    notification.seen = True
    notification.save()
    return redirect('/notifications')


   


