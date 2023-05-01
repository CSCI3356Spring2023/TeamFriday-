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
    path("instructor_summary/application/<int:pk>", views.ApplicationDetail.as_view(), name="application detail"),
    path("instructor_summary/application/resume/<int:pk>", views.show_pdf, name="application detail"),
    path("apply/error/",login_required(views.app_error.as_view()),name="apply error"),
    path("accept_offer/<int:application>/", views.accept_offer, name="accept_offer"),
    path("reject_offer/<int:application>/", views.reject_offer, name="reject_offer"),
    
]