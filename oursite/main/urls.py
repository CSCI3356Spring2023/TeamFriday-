from django.urls import path 
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("", views.fp, name="front page"),
    path("home/",login_required(views.CourseListView.as_view()),name="home page"),
    path("apply/<int:id>",views.apply, name="apply"),
    path("instructor_summary/",views.InstructorSummaryView, name="instructor_summary"),
    path("apply/error/",login_required(views.app_error.as_view()),name="apply error"),

    
]