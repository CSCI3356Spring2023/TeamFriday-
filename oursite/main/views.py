from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, addCourseForm
from .models import Course
from django.views.generic import CreateView

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

def upload_file(request):
    if request.method == "POST":
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect("/success/url/")
    else:
        form = ModelFormWithFileField()
    return render(request, "upload.html", {"form": form})

# Create your views here.
@login_required(login_url='login/')
def home(response):
    return render(response, 'main/home.html', {})


def fp(response):
    return render(response, 'main/fp.html', {})
# StudentSignupView

# CreateCourseView
class addCourse(CreateView):
    model = Course
    form_class = addCourseForm
    template_name = 'main/addcourse.html'

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return redirect('/')


# CreateApplicationView

# InstructorSignupView

# Student signup
# Admin signup




