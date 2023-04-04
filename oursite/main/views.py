from django.shortcuts import render, redirect
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.views.generic import ListView
from .models import Course

from .forms import UploadFileForm, addCourseForm, StudentSignUpForm, InstructorSignUpForm, AdminSignUpForm, CreateApplicationForm
from .models import User, Student, Instructor, Admin, Course, Application

from django.core.mail import send_mail


# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

# def handle_uploaded_file(f):
#     with open("some/file/name.txt", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

# def upload_file(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES["file"])
#             return HttpResponseRedirect("/success/url/")
#     else:
#         form = UploadFileForm()
#     return render(request, "upload.html", {"form": form})

# def upload_file(request):
#     if request.method == "POST":
#         form = ModelFormWithFileField(request.POST, request.FILES)
#         if form.is_valid():
#             # file is saved
#             form.save()
#             return HttpResponseRedirect("/success/url/")
#     else:
#         form = ModelFormWithFileField()
#     return render(request, "upload.html", {"form": form})

# Create your views here.
@login_required()
def home(response):
    return render(response, 'main/home.html', {})


def fp(response):

    if response.user.is_authenticated:
        return redirect('/home')

    return render(response, 'main/fp.html', {})
# StudentSignupView

# CreateCourseView
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

	# email
	email = self.request.user.email
	send_mail(
		'Subject: Successfully Created Course',
		course_code,
		'BCEagleHire@gmail.com'
		email,
		fail_silently=False,
	}
		

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

        return redirect('/home')



def apply(response, id):
    if response.method == "POST":
        form = CreateApplicationForm(response.POST, response.FILES)
        course = Course.objects.get(id=id)
        apps = Application.objects.filter(user=response.user)
        app_count = len(apps)

        if form.is_valid() and app_count < 5:
            application = Application(course_name = course.course_code, user=response.user)
            resume = response.FILES['resume']
            application.resume = resume
            application.save()
            course.applications.add(application)
            course.save()
        return redirect('/home')
    else:
            form = CreateApplicationForm()

    return render(response, "main/create_app.html",{'form':form})   

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

        return redirect('/home')

class CourseListView(ListView):
    model = Course
    template_name = 'main/home.html'
    context_object_name = 'courses'

def InstructorSummaryView(response):
    # model = Course
    # template_name = 'main/Instructor_Summary.html'
    # context_object_name = 'courses'

    # def get_context_data(self, **kwargs):
    #     context = super(InstructorSummaryView, self).get_context_data(**kwargs)
    #     courses = Course().objects.filter(user = self.request.user)
    #     apps = []
    #     for course in courses:
    #         apps.extend(course.application.all())
    #     context['applications'] = apps

    #     return context

    context = {}
    if response.method == "GET" :
        courses = Course.objects.filter(user = response.user)
        apps = []
        for course in courses:
            apps.extend(course.applications.all())
        context['applications'] = apps
        context['courses'] = courses
    return render(response, "main/Instructor_Summary.html",context)


